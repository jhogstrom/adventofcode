from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = True
stardate = "X"
year = "YEAR"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
