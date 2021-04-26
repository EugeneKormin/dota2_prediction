import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier

from hyperopt import hp, tpe
from hyperopt.fmin import fmin

# Для теста возьмем классический сет "ирисы Фишера"
# Разумеется вместо X и y Вам следует взять свои фичи и таргет
iris = datasets.load_iris()
X = iris.data
y = iris.target


def hyperopt_xgb_score(params):
    clf = XGBClassifier(**params)
    # усреднение по 3ем фолдам, для уменьшения влияния стахостичности
    # для ускорения можно использовать train_test_split один раз
    current_score = cross_val_score(clf, X, y, cv=3).mean()
    print(current_score, params)
    return -current_score


simple_space_xgb = {
    'n_estimators': hp.choice('n_estimators', range(100, 1000)),
    'eta': hp.quniform('eta', 0.025, 0.5, 0.025),
    'max_depth': hp.choice('max_depth', np.arange(1, 14, dtype=int)),
}

best = fmin(fn=hyperopt_xgb_score, space=simple_space_xgb, algo=tpe.suggest, max_evals=10)
print('best:')
print(best)