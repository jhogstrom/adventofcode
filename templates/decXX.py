import os
from timer import timeit
from collections import defaultdict, deque

stardate =
dataname = f"dec{stardate}.txt"
dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

@timeit
def star1(data):
    ...


@timeit
def star2(data):
    ...

star1(data)
star2(data)