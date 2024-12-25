import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "23"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    groups = [set(_.split("-")) for _ in data]
    i = 0
    result = []
    while i < len(groups):
        j = i + 1
        while j < len(groups):
            if any(_ in groups[i] for _ in groups[j]):
                group = groups[i].union(groups[j])
                if any(_.startswith("t") for _ in group):
                    k = j + 1
                    while k < len(groups):
                        if all(_ in group for _ in groups[k]):
                            s = ", ".join(sorted(group))
                            result.append(s)
                        k += 1
            j += 1
        i += 1
        print(i, end="\r")

    for _ in sorted(result):
        print(_)

    print(len(set(result)))


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
