import os
from timer import timeit

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec1.txt'
data = [int(_) for _ in open(filename, 'r').readlines()]

# data = [
#     199,
# 200,
# 208,
# 210,
# 200,
# 207,
# 240,
# 269,
# 260,
# 263
# ]

@timeit
def star1():
    increase_count = 0
    for d in range(len(data)):
        if d == 0:
            continue
        if data[d-1] < data[d]:
            increase_count += 1
        # print(f"{data[d-1]} {data[d]}, {data[d-1] < data[d]}")

    print(increase_count)



@timeit
def star2():
    increase_count = 0
    for d in range(len(data)):
        if d < 2:
            continue

        d1 = sum([data[d-3], data[d-2], data[d-1]])
        d2 = sum([data[d-2], data[d-1], data[d]])
        if d1 < d2:
            increase_count += 1
        # print(f"{d1} {d2}, {d1 < d2}")
    return increase_count

    print(increase_count)


star1()
print(star2())