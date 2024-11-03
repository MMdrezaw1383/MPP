from functools import reduce

def reverse():
    s = "mmd"
    s = "".join(reversed(s))
    print(s)

def reversed_by_for():
    s = "mmd"
    rs = ""
    for i in s:
        rs = i + rs
    print(rs)

def reversed_by_reduce():
    s = 'mmd'
    print(reduce(lambda x, y: y + x, s))

def reversed_by_slice():
    s = 'mmd'
    s = s[::-1]
    print(s)
