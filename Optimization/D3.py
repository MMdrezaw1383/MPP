def create_dict():
    names = ['ali', 'mmd', 'ahmad']
    ages = [20, 21, 22]
    d = dict(zip(names, ages))
    print(d)


# ---------------------------------
import itertools


def list_items():
    lst = [[1, 2, 3], (1, 2, 3), ]
    ls = list(itertools.chain.from_iterable(lst))
    print(ls)


# ---------------------------------
d1 = {'mmd': 24, "ali": 19}
d2 = {'ahmad': 66}


def reverse_dict1(d):
    d = {v: k for k, v in d.items()}
    print(d)


def reverse_dict2(d):
    d = dict((v, k) for k, v in d.items())
    print(d)


def reverse_dict3(d):
    d = dict(map(reversed, d.items()))
    print(d)


# ---------------------------------
def compound2dict(d1, d2):
    d3 = d1 | d2
    d4 = {**d1, **d2}
    d1.update(d2)
    print(d1)
    print(d3)
    print(d4)


# ---------------------------------
