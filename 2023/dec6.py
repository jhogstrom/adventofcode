import logging
from math import prod
from reader import get_data, timeit, set_logging

runtest = False
stardate = "6"

set_logging(runtest)
data = get_data(stardate, "2023", runtest)


def parsedata(data):
    times = [int(_) for _ in data[0].split(":")[1].split()]
    dist = [int(_) for _ in data[1].split(":")[1].split()]
    return list(zip(times, dist))


def get_combos(time, dist):
    return len([_ for _ in range(1, time-1) if (time-_) * _ > dist])


@timeit
def star1(data):
    logging.debug("running star 1")
    print(prod([get_combos(*_) for _ in parsedata(data)]))


@timeit
def star2(data):
    logging.debug("running star 2")
    t = int(data[0].split(":")[1].replace(" ", ""))
    d = int(data[1].split(":")[1].replace(" ", ""))
    print(get_combos(t, d))


star1(data)
star2(data)
