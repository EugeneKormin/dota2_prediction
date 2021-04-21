
def train_test_split_timerows(list_1, divide):
    split = int(len(list_1) * divide)
    train, test = list_1[:split], list_1[split:]
    return train, test
