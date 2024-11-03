from contextlib import suppress

x = 5
y = 0


# 1
def zero_error():
    try:
        print(x / y)
    except ZeroDivisionError:
        print("error")

    print(x / y) if y != 0 else print("error")


# 2
def exec_():
    exec("try:print(x / y)\nexcept ZeroDivisionError:print('error')")


# 3
def sup():
    with suppress(ZeroDivisionError): print(x / y)


# -------------------
import numpy as np


def np_ages():
    ages = [20, 19, 140]
    for i in range(len(ages)):
        if ages[i] > 100:
            ages[i] = 0


def np_ages1():
    ages1 = np.array([20, 19, 140])
    ages1 = np.where(ages1 > 120, 0, 1)
    print(ages1)


def np_ages2():
    ages2 = np.array([20, 19, 140])
    ages2[ages2 < 120] = 1
    ages2[ages2 > 120] = 0
    print(ages2)
# -------------------
