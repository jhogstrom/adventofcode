import logging
import operator  # noqa E401
from functools import reduce
from itertools import combinations

from reader import get_data, set_logging, timeit

runtest = False
stardate = "24"
year = "2015"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    packets = [int(_) for _ in data]
    one_third = sum(packets) // 3
    packets.sort(reverse=True)
    shortest = len(packets)
    qe = reduce(operator.mul, packets, 1)
    for i in range(1, len(packets)):
        for c in combinations(packets, i):
            if sum(c) == one_third:
                if len(c) <= shortest:
                    shortest = len(c)
                    new_qe = reduce(operator.mul, c, 1)
                    if new_qe < qe:
                        qe = new_qe
                        # print(c, qe)
                else:
                    if shortest < len(packets):
                        return qe


@timeit
def star2(data):
    logging.debug("running star 2")
    packets = [int(_) for _ in data]
    one_quarter = sum(packets) // 4
    packets.sort(reverse=True)
    shortest = len(packets)
    qe = reduce(operator.mul, packets, 1)
    for i in range(1, len(packets)):
        for c in combinations(packets, i):
            if sum(c) == one_quarter:
                if len(c) <= shortest:
                    shortest = len(c)
                    new_qe = reduce(operator.mul, c, 1)
                    if new_qe < qe:
                        qe = new_qe
                        # print(c, qe)
                else:
                    if shortest < len(packets):
                        return qe


print(star1(data))
print(star2(data2))
