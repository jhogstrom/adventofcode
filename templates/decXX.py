from collections import defaultdict, deque
import logging
from reader import get_data, timeit

runtest = False
stardate = "X"

data = get_data(stardate, runtest)
data2 = data[:]


@timeit
def star1(data):
    ...


@timeit
def star2(data):
    ...


star1(data)
star2(data2)
