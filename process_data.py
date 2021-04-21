def train_test_split_timerows(X, y, divide):
    split = int(len(X) * divide)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    return X_train, X_test, y_train, y_test

