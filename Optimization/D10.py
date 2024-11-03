s = "im mmdrezaw"


# 1
def open_file1():
    f = open("new_tex.txt", "w").write(s)


# 2
def open_file2():
    with open("new_tex.txt", "w") as file: file.write(s)


# 3
def open_file3():
    print(s, file=open("new_text.txt", "w"))


# -------------------

def input_list():
    li = list(map(int, input("enter number: ").split()))
    print(li)
    print(type(li[0]))


# ---------------------
def read_file():
    with open("new_text.txt", "r") as f:
        for i, line in enumerate(f, 1):
            if i == 1:
                line1 = line
                break
    print(line1)


import linecache


def read_file2():
    line1 = linecache.getline("new_text.txt", 1)
    print(line1)


# ------------------
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.ave = 0

    def cave(self):
        return self.ave + 10


St = type("Student", (object,), {"name": 'ali', "age": 13, "ave": 0, "cave": lambda self: self.ave + 10})
def stu_():
    s1 = St()
    print(s1.cave())


# ------------------
class Mmd1:
    def __init__(self, a, b):
        self.__dict__.update({k: v for k, v in locals().items() if k != "self"})


class Mmd2:
    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
# ---------------------------
