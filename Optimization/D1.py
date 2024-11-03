from pprint import pprint


def exchange2var():
    a = 6
    b = 4
    a, b = b, a


# ---------
def multi_vars():
    d, e, *c = 1, 2, 3, 4, 5
    f, g, *h = {'s': 1, 'n': 2, 'j': 4, '9': 6}


# ---------
def walrus():
    while "y" in (answer := input("enter yes to continue").lower()):
        x = int(input("enter a number: "))
        print(x ** 2)


# ---------
def chain_operators():
    x = 5
    if 3 > x < 10:
        return 'yes'


# ----*-----
def most_frequent():
    li = [1, 2, 3, 1, 1, 2, 1]
    print(max(set(li), key=li.count))


# ---------
def transposed():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    pprint(matrix, width=20)
    # 3 = columns ->
    transpose = [[row[i] for row in matrix] for i in range(3)]
    print('\n', '\n')
    pprint(transpose, width=20)
    # -------zip
    pprint(list(zip(*matrix)), width=20)



