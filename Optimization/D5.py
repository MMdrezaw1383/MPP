def all_elements_same():
    lst = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    return all(x == lst[0] for x in lst)
    # return len(set(lst)) == 1


print(all_elements_same())


# -----------
def mapfilter_comprehension():
    lst = [2, 4, 6, 5, 3, 1]
    squares = [i ** 2 for i in lst if i % 2 == 0]
    squares_map = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, lst)))
    print(squares)
    print(squares_map)
    squares_dict = {i: i ** 2 for i in lst if i % 2 == 0}
    print(squares_dict)


# -----------
def compare_list():
    pass


# ------------
def is_rejected():
    scores = [17, 18, 19, 20, 16]

    print(any(score < 17 for score in scores))


def is_accepted():
    scores = [17, 18, 19, 20, 16]

    print(all(score > 17 for score in scores))


# ------------------
def ternary():
    # x if (condition) else y
    # list -> (x,y)[condition]
    x, y = 8, 5
    m = x if x < y else y
    print("min: ", m)
    # m2 = (x,y)[True]
    m2 = (y, x)[x < y]
    print("min:", m2)

