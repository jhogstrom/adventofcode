import os
from timer import timeit
from collections import defaultdict

stardate = 7
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
data = [int(_) for _ in data[0].split(",")]


def calc_cost(p, data, calculator):
    return sum(calculator(abs(_-p)) for _ in data)


@timeit
def calculate(data, calculator):
    print(int(min( [calc_cost(p, data, calculator) for p in range(min(data), max(data)+1)])))


calculate(data, lambda x: x)
calculate(data, lambda p: p * (1 + p) / 2)