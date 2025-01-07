import hashlib
import logging
from collections import defaultdict

from reader import get_data, set_logging, timeit

runtest = False
stardate = "14"
year = "2016"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")


@timeit
def star2(data):
    logging.debug("running star 2")
    salt = data[0]
    index = 0
    keys = []
    hashes = defaultdict(str)
    while len(keys) < 64:
        if index not in hashes:
            hashes[index] = salt + str(index)
            for _ in range(2017):
                hashes[index] = hashlib.md5(hashes[index].encode()).hexdigest()
        h = hashes[index]
        for i in range(len(h) - 2):
            if h[i] == h[i + 1] == h[i + 2]:
                for j in range(index + 1, index + 1001):
                    if j not in hashes:
                        hashes[j] = salt + str(j)
                        for _ in range(2017):
                            hashes[j] = hashlib.md5(hashes[j].encode()).hexdigest()
                    if h[i] * 5 in hashes[j]:
                        keys.append(h)
                        break
                break
        index += 1
    print(index - 1)


star1(data)
star2(data2)
