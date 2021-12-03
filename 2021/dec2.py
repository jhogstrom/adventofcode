import os
from timer import timeit

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec2.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
#     "forward 5",
# "down 5",
# "forward 8",
# "up 3",
# "down 8",
# "forward 2",
# ]

@timeit
def star1():
    dep, hor = 0, 0
    for c in data:
        cmd, val = c.split()
        val = int(val)
        if cmd == "forward":
            hor += val
        elif cmd == "back":
            hor -= val
        elif cmd == "up":
            dep -= val
        elif cmd == "down":
            dep += val
        else:
            raise ValueError(c)

    print(dep, hor, dep * hor)

@timeit
def star2():
    dep, hor, aim = 0, 0, 0
    for c in data:
        cmd, val = c.split()
        val = int(val)
        if cmd == "forward":
            hor += val
            dep += aim * val
        elif cmd == "back":
            hor -= val
        elif cmd == "up":
            aim -= val
        elif cmd == "down":
            aim += val
        else:
            raise ValueError(c)

    print(dep, hor, dep * hor)


star1()
star2()