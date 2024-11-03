from pprint import pprint
from operator import itemgetter
import heapq


def cr_matrix():
    matrix = [[0] * 3, [0] * 3, [0] * 3]
    matrix2 = [[0 for i in range(10)] for j in range(10)]
    pprint(matrix, width=40)
    print("*" * 10)
    pprint(matrix2, width=40)


# -----
def differences():
    lst1 = [1, 2, 3, 4, 5, 10]
    lst2 = [1, 1, 4, 5]
    lst3 = list(set(lst1).symmetric_difference(lst2))
    print(lst3)


# ------
def cycle_list():
    lst = [1, 2, 3, 4, 5, 6]
    print(lst[4:] + lst[:4])
    print(lst[-4:] + lst[:-4])


# ----------
def find_n_largest():
    x = [-3, 10, 2, 8, 0, 3]
    final_list = x.copy()
    final_list.sort()
    final_list = final_list[-3:]

    final_list2 = heapq.nlargest(3, x)
    final_list3 = heapq.nsmallest(3, x)
    print(final_list)
    print(final_list2)

# -----------
import json
import ast


def str2list():
    s = "[1,2,[4,5,6]]"
    lst = json.loads(s)

    lst2 = ast.literal_eval(s)
    print(type(lst))
    print(type(lst2))


# --------
def sort_dict():
    d = {'b': 2, 'a': 1, 'c': 3, 'd': 4}
    sorted_dict = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
    sorted_dict2 = {k: d[k] for k in sorted(d, key=d.get)}
    sorted_dict3 = dict(sorted(d.items(), key=itemgetter(1)))
    print(sorted_dict)
    pprint(sorted_dict2)
    pprint(sorted_dict3)


# ----------
def roundminous():
    print(round(18909.456790, -3))


# -----------
t = "Artificial Intelligence (AI) refers to the development of computer systems\
capable of performing tasks that typically require human intelligence.\
These tasks include learning from experience (machine learning),\
understanding natural Language, recognizing patterns, and problem-solving.\
The goal of AI is to create machines that can perform cognitive functions\
similar to those of humans. Machine learning algorithms enableAI systems\
to analyze data, identify patterns, and make decisions without explicit programming,"
search = lambda text, query: text[text.find(query) - 20: text.find(query) + 20] if query in text else -1
# print(search(t, 'those'))
