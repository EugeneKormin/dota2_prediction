import matplotlib.pyplot as plt
from numpy import sin, cos, pi, arange


def hours_to_sin(hours):
    res_sin = sin(2 * pi * hours / 24)
    print(res_sin)

