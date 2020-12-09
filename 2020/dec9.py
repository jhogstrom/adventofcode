import os
import itertools
from timing import timeit
import logging

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [int(_.strip()) for _ in open(filename, 'r').readlines()]
preamble_size = 25

# data = [
#         35,
#         20,
#         15,
#         25,
#         47,
#         40,
#         62,
#         55,
#         65,
#         95,
#         102,
#         117,
#         150,
#         182,
#         127,
#         219,
#         299,
#         277,
#         309,
#         576
#     ]
# preamble_size = 5

preamble = data[:preamble_size]

@timeit
def parse():
    data = [int(_.strip()) for _ in open(filename, 'r').readlines()]
    preamble_size = 25
    preamble = data[:preamble_size]

@timeit
def star1():
    global preamble
    for n in data[preamble_size:]:
        sums = [sum(_) for _ in itertools.combinations(preamble, 2)]
        if n in sums:
            preamble = preamble[1:] + [n]
        else:
            print(f"* {n}")
            return n


@timeit
def star2(target):
    c = 0
    for i in range(len(data)-1):
        for j in range(len(data)):
            c += 1
            _sum = sum(data[i:j])
            if _sum > target:
                break
            if _sum == target:
                print(f"** {min(data[i:j]) + max(data[i:j])}")
                return


parse()
n = star1()
star2(n)