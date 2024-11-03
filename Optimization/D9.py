import time
import timeit
import collections
from getpass import getpass
from itertools import combinations
import random
import secrets
import string
import binascii
import codecs
from pympler import asizeof, muppy, summary


def get_pass():
    password = getpass()
    print(password)


# ----------------

# time.perf_counter()
# time.process_time()
def func():
    pass


# print(timeit(stmt="func()", globals=globals(), number=2))

# -----------------
def collections_count():
    lst = ['a', 'ab', 'b', 'a', 'c', 'b', 'b', 'b']
    print(collections.Counter(lst))


# ------------------
def get_pwsets():
    s = {'a', 'b', 'c'}
    print(list(combinations(s, r=2)))


# -------------------

def create_pass():
    password = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))
    print(password)
    safe_password = "".join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))
    print(safe_password)


# ---------------------
def hex_to_dec1(star=True):
    hex_str = "69016d"
    byte_array = bytes.fromhex(hex_str)
    text = byte_array.decode('utf-8')
    print(text)


def hex_to_dec2():
    hex_str = "69016d"
    byte_array = binascii.unhexlify(hex_str)
    text = byte_array.decode('utf-8')
    print(text)


def hex_to_dec3():
    hex_str = "4920616d"
    byte_array = codecs.decode(hex_str, 'hex')
    text = byte_array.decode('utf-8')
    print(text)


def hex_to_dec4():
    hex_str = "4920616d"
    text = ("".join(chr(int(hex_str[i:i + 2], 16)) for i in range(0, len(hex_str), 2)))
    print(text)


# ------------------------
def size_of_objects():
    s = "str masala"
    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)
    sum1 = summary.summarize(s)
    summary.print_(sum1)
# ----------------------------
