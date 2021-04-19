def dec2(f):
    def new_f():
        print("Decorating", f.__name__)
        f()
    return new_f

@dec2
def func2():
    print("inside func2()")

func2()