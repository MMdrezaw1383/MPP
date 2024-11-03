from itertools import zip_longest


def ternary2():
    # x and y return x if x is False
    # x or y return x if x is True
    # condition and x or y
    # *
    # x if condition1 else y condition2 if condition3 else z
    x, y = 8, 12
    m = x < y and x or y
    m2 = (x < y and [x] or [y])[0]
    print(m2)


# -----------
def else_():
    for i in range(3):
        print(i)
    else:
        print("halghe kamel ejra shod")


# -----------
def zip_iterator():
    names = ["mmd", "ali", "reza"]
    ages = [10, 20]
    max_age = 0
    greatest_person = None
    for name, age in zip_longest(names, ages, fillvalue=0):
        if age > max_age:
            max_age = age
            greatest_person = name
    print(list(zip_longest(names, ages, fillvalue=0)))
    print(greatest_person)