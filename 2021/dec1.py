import os
from timer import timeit

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec1.txt'
data = [int(_) for _ in open(filename, 'r').readlines()]


@timeit
def star1():
    increase_count = 0
    for d in range(1, len(data)):
        if data[d-1] < data[d]:
            increase_count += 1
    print(increase_count)



@timeit
def star2():
    increase_count = 0
    for d in range(2, len(data)):
        # d1 = sum([data[d-3], data[d-2], data[d-1]])
        # d2 = sum([           data[d-2], data[d-1], data[d]])
        if data[d-3] < data[d]:
            increase_count += 1

    print(increase_count)


star1()
star2()