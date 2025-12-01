import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = True
stardate = "19"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]
invalid = set()


def parse_data(data):
    designs = [_.strip() for _ in data[0].split(",")]
    patterns = data[2:]
    return designs, patterns


def can_make(designs, pattern):
    if len(pattern) == 0:
        return True

    for d in designs:
        if pattern.startswith(d) and pattern not in invalid:
            if can_make(designs, pattern[len(d) :]):  # noqa e203
                return True
            else:
                invalid.add(pattern[len(d) :])  # noqa e203
    return False


@timeit
def star1(data):
    logging.debug("running star 1")
    designs, patterns = parse_data(data)

    result = 0
    for pattern in patterns:
        if can_make(designs, pattern):
            result += 1
        # invalid.clear()
    print(result)


valid = defaultdict(int)


def can_make2(designs, pattern):
    # print(pattern)
    if len(pattern) == 0:
        return 1

    res = 0
    for d in designs:
        if pattern.startswith(d) and pattern not in invalid:
            if pattern in valid:
                res += valid[pattern]
            else:
                r = can_make2(designs, pattern[len(d) :])  # noqa e203
                if r:
                    res += r
                    p = pattern[len(d) :]  # noqa e203
                    if p:
                        valid[p] += r
                else:
                    invalid.add(pattern[len(d) :])  # noqa e203
    return res


@timeit
def star2(data):
    logging.debug("running star 2")
    designs, patterns = parse_data(data)
    valid.clear()
    # print(can_make2(designs, "bgbr"))
    # exit()
    result = 0
    i = 0
    for pattern in patterns:
        r = can_make2(designs, pattern)
        result += r
        print(r, pattern)
        i += 1
        # print(i)
    print(result)


star1(data)
star2(data2)
