import sys
import pprint
from functools import lru_cache
sys.setrecursionlimit(10)

# -------
x = [
    "mmd is the best",
    "mmd for ever",
    " ff"
]

results = list(map(lambda s: (True, s) if 'mmd' in s else (False, s), x))
# print(results)

# -----------
@lru_cache(maxsize=None)
def fib():
    pass

# ------------
