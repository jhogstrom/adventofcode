from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "6"

set_logging(runtest)
data = get_data(stardate, runtest)
data2 = data[:]

def parsedata(data):
    times = [int(_) for _ in data[0].split(":")[1].split()]
    dist = [int(_) for _ in data[1].split(":")[1].split()]
    return list(zip(times, dist))


def get_combos(time, dist):
    d, res = 0, 0
    for t in range(1, time-1):
        d = (time-t) * t
        # logging.debug(f"{t} => {d}")
        if d > dist:
            res += 1
    return res

@timeit
def star1(data):
    logging.debug("running star 1")
    races = parsedata(data)
    res = 1
    for _ in races:
        r = get_combos(_[0], _[1])
        logging.debug(f"{_} => {r}")
        res *= r
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    t = int(data[0].split(":")[1].replace(" ", ""))
    d = int(data[1].split(":")[1].replace(" ", ""))
    r = get_combos(t, d)
    print(r)

star1(data)
star2(data2)
