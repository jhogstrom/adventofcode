import logging

from reader import get_data, set_logging, timeit

# from collections import defaultdict, deque


runtest = True
stardate = "12"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def count_combinations(s, combos):
    print(f"s, combos: <{s}>, {combos}")
    groups = [_ for _ in s.split(".") if _ != ""]
    print(groups)
    # group = 0
    # for c in s:
    #     if c == "?":
    #         c = "."

    return 0


@timeit
def star1(data):
    logging.debug("running star 1")
    res = 0
    for _ in data:
        p = _.split()
        res += count_combinations(p[0], [int(s) for s in p[1].split(",")])
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
