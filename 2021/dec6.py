import os
from timer import timeit
from collections import defaultdict

stardate = 6
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
data = [int(_) for _ in data[0].split(",")]


@timeit
def star1(data):
    for day in range(80):
        nextday = []
        fishspawned = 0
        for fish in data:
            if fish == 0:
                nextday.append(6)
                fishspawned += 1
            else:
                nextday.append(fish-1)
        nextday.extend([8]*fishspawned)
        data = [*nextday]
    print(len(data))


@timeit
def star2(data, days):
    bucket = defaultdict(int)
    for _ in data:
        bucket[_] += 1

    for day in range(1, days+1):
        d0 = bucket[0]
        bucket[0] = bucket[1]
        bucket[1] = bucket[2]
        bucket[2] = bucket[3]
        bucket[3] = bucket[4]
        bucket[4] = bucket[5]
        bucket[5] = bucket[6]
        bucket[6] = bucket[7] + d0
        bucket[7] = bucket[8]
        bucket[8] = d0

    print(day, sum(bucket.values()))


star1(data)
star2(data, 80)
star2(data, 256)