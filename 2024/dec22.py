import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "22"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def make_secret(n, c) -> int:
    for _ in range(c):
        n = ((n << 6) ^ n) % 16777216
        n = ((n >> 5) ^ n) % 16777216
        n = ((n << 11) ^ n) % 16777216
    return n


@timeit
def star1(data):
    logging.debug("running star 1")
    initial_numbers = [int(_) for _ in data]
    result = 0
    for n in initial_numbers:
        r = make_secret(n, 2000)
        result += r
    print(result)


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
