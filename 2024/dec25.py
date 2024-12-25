import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "25"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def parse(data):
    columns = [-1] * 5
    for c in range(5):
        for line in range(0, 7):
            if data[line][c] == "#":
                columns[c] += 1

    return data[0][0] == "#", columns


@timeit
def star1(data):
    logging.debug("running star 1")
    i = 0
    keys = []
    locks = []
    while i < len(data):
        is_key, pattern = parse(data[i : i + 7])  # noqa E203
        if is_key:
            keys.append(pattern)
        else:
            locks.append(pattern)
        i += 8

    res = 0
    for key in keys:
        for lock in locks:
            if all(key[i] + lock[i] <= 5 for i in range(5)):
                res += 1
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
