from timer import timeit
from collections import defaultdict, deque
import logging
from reader import get_data

runtest = False
stardate = "X"

data = get_data(stardate, runtest)


@timeit
def star1(data):
    ...


@timeit
def star2(data):
    ...


data2 = data[:]


star1(data)
star2(data2)