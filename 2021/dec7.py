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


def calc_cost(p, data, fuel_cost):
    return sum(fuel_cost(abs(_-p)) for _ in data)


@timeit
def calculate(data, calculator):
    print(min([calc_cost(p, data, calculator) for p in range(min(data), max(data)+1)]))


# Cost is number of steps
calculate(data, lambda steps: steps)
# Cost is 1+2+3+...+steps
calculate(data, lambda steps: steps * (1 + steps) // 2)