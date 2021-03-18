import pandas as pd
from main import run


x = 4


class Main(object):
    def __init__(self, x):
        self.x = x

    def func(self):
        print(self.x)


main = Main(x=x)
main.func()

print(Main(x=x).__dict__)
print(main.__dict__)
print(main.func().__dict__)
