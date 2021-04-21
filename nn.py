from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.activations import elu, gelu, selu, softmax
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from get_data import get
from process_data import train_test_split_timerows


df = get()
scaler = StandardScaler()

initial_learning_rate = 0.00001
epochs = 300


X = df.drop(["radiant_win"], axis=1)
y = df["radiant_win"]

X["series_id"] = X["series_id"].astype(str)
X["league_id"] = X["league_id"].astype(str)
X["radiant_team_id"] = X["radiant_team_id"].astype(str)
X["dire_team_id"] = X["dire_team_id"].astype(str)


X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split_timerows(X=X, y=y, divide=.7)
X_test, X_val, y_test, y_val = train_test_split_timerows(X=X_test, y=y_test, divide=.7)


def lr_time_based_decay(epoch, lr):
    return lr


model = Sequential()
model.add(Dense(32, activation=gelu))
model.add(Dropout(.5))
model.add(Dense(16, activation=gelu))
model.add(Dropout(.5))
model.add(Dense(1, activation=gelu))
model.compile(
    loss="mae",
    optimizer="adam"
)

history = model.fit(
    X_train, y_train,
    epochs=epochs,
    batch_size=16,
    validation_data=(X_test, y_test),
    verbose=1,
    callbacks=[LearningRateScheduler(lr_time_based_decay, verbose=1)]
)

y_val_list = list(range(len(history.history["loss"])))

x_loss_list = history.history["loss"]
x_loss_val_list = history.history["val_loss"]

plt.plot(y_val_list, x_loss_list, marker='o', color="blue", label='train')
plt.plot(y_val_list, x_loss_val_list, marker='o', color="red", label='val')

plt.legend()

plt.show()

correct_preds = 0
total = 0
y_pred = model.predict(X_val)
for i in zip(y_pred, y_val):
    prediction = float(i[0])
    if prediction > .5:
        print("right")
        pred = True
    elif prediction < .5:
        print("wrong")
        pred = False
    if pred == bool(i[1]):
        correct_preds += 1
    total += 1


print(round(correct_preds / total * 100, 2))
