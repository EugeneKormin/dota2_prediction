from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.activations import elu, gelu, selu, softmax, sigmoid
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from hyperopt import Trials, hp, fmin, tpe, STATUS_OK
from numpy import argmin


from get_data import get
from process_data import train_test_split_timerows


df = get()
scaler = StandardScaler()

initial_learning_rate = 0.00001
epochs = 50

X = df.drop(["radiant_win"], axis=1)

y = df["radiant_win"]

X["series_id"] = X["series_id"].astype(str)
X["league_id"] = X["league_id"].astype(str)
X["radiant_team_id"] = X["radiant_team_id"].astype(str)
X["dire_team_id"] = X["dire_team_id"].astype(str)

X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split_timerows(X=X, y=y, divide=.8)
X_test, X_val, y_test, y_val = train_test_split_timerows(X=X_test, y=y_test, divide=.8)


def lr_time_based_decay(epoch, lr):
    return lr


def run_model(space):
    model = Sequential()
    layer_size = space["layer_size"]
    layer_num = space["layers_num"]
    learning_rate = 10 ** -space["learning_rate"]

    for layer_num in range(layer_num):
        layers = 2 ** layer_size
        layer_size -= 1
        model.add(Dense(layers, activation=space["activation_function_" + str(layer_num + 1)]))
    layer_num += 1
    model.add(Dense(1, activation=sigmoid))

    if space["optimizer"] == "SGD":
        optimizer = SGD(learning_rate=learning_rate)
    elif space["optimizer"] == "Adam":
        optimizer = Adam(learning_rate=learning_rate)
    elif space["optimizer"] == "RMSprop":
        optimizer = RMSprop(learning_rate=learning_rate)

    model.compile(
        loss="mse",
        optimizer=optimizer
    )

    batch_size = 2**space["batch_size"]
    epochs = 2**space["epochs"]

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        verbose=0,
        callbacks=[LearningRateScheduler(lr_time_based_decay, verbose=1)]
    )

    y_val_list = list(range(len(history.history["loss"])))

    x_loss_list = history.history["loss"]
    x_loss_val_list = history.history["val_loss"]

    plt.plot(y_val_list, x_loss_list, marker='o', color="blue", label='train')
    plt.plot(y_val_list, x_loss_val_list, marker='o', color="red", label='val')

    plt.legend()

    wrong_preds = 0
    correct_preds = 0
    error = 0
    total = 0

    y_pred = model.predict(X_val)
    for i in zip(y_pred, y_val):
        pred = i[0][0]
        actual = i[1]
        if (pred > .5 and actual > .5) or (pred < .5 and actual < .5):
            correct_preds += 1
            error += (abs(pred) - actual) ** 2
        else:
            wrong_preds += 1
            error += (abs(pred) + 1) ** 2

        total += 1

    percent = round((correct_preds / total) * 100, 2)
    print(f"error: {error}/ correct_preds: {correct_preds}/ wrong_preds: {wrong_preds}/ percent: {percent}"
          .format(error=error / total, correct_preds=correct_preds, wrong_preds=wrong_preds, percent=percent))

    score = round(error, 2)
    data_to_return = {
        "loss": score,
        "model": model,
        "status": STATUS_OK
    }
    return data_to_return


nn_space = {
    "activation_function_1": hp.choice("activation_function_1", [elu, gelu, selu]),
    "activation_function_2": hp.choice("activation_function_2", [elu, gelu, selu]),
    "activation_function_3": hp.choice("activation_function_3", [elu, gelu, selu]),
    "activation_function_4": hp.choice("activation_function_4", [elu, gelu, selu]),
    "activation_function_5": hp.choice("activation_function_5", [elu, gelu, selu]),
    "activation_function_6": hp.choice("activation_function_6", [elu, gelu, selu]),
    "activation_function_7": hp.choice("activation_function_7", [elu, gelu, selu]),
    "last_layer_activation_function": hp.choice("last_layer_activation_function", [elu, gelu, selu, softmax]),
    "loss": hp.choice("loss", ["mae"]),
    "optimizer": hp.choice("optimizer", ["SGD", "Adam", "RMSprop"]),
    "batch_size": hp.choice("batch_size", range(4, 6)),
    "epochs": hp.choice("epochs", range(2, 7)),
    "layers_num": hp.choice("layers_num", range(3, 8)),
    "learning_rate": hp.choice("learning_rate", range(3, 11)),
    "layer_size": hp.choice("layer_size", range(4, 10))
}

trials = Trials()

best = fmin(trials=trials, fn=run_model, space=nn_space, algo=tpe.suggest, max_evals=2)

best_trial_loss = 1e+6
best_model = Sequential().compile()

for trial in trials:
    current_trial_loss = trial["result"]["loss"]
    if best_trial_loss > current_trial_loss:
        best_trial_loss = current_trial_loss
        best_model = trial["result"]["model"]

print(best_model)
print(best_trial_loss)
