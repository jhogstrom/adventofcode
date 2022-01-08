import os
from timer import timeit
from collections import defaultdict, deque

stardate = 11
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
# dataname = f"dec{stardate}_test2.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

maxx = maxy = 0
def parse_data(data) -> dict:
    global maxx
    global maxy
    res = {}
    for y, _ in enumerate(data):
        for x, c in enumerate(data[y]):
            res[(x, y)] = int(c)
    maxx, maxy = x+1, y+1
    return res


def printgrid(data, gen):
    print(f"===After step {gen}:")
    for y in range(maxy):
        for x in range(maxx):
            print(data[(x, y)], end="")
        print()
    print()


def inboard(c) -> bool:
    x, y = c[0], c[1]
    return 0 <= x < maxx and 0 <= y < maxy


def get_neighbors(c) -> list:
    x, y = c[0], c[1]
    return [
        (x-1, y-1),
        (x,   y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x,   y+1),
        (x+1, y+1),
    ]


def do_flash(data, coord, flashed):
    flashed.append(coord)
    for n in get_neighbors(coord):
        if inboard(n):
            data[n] += 1
            if data[n] > 9 and n not in flashed:
                do_flash(data, n, flashed)


def reset_flashers(data, flashed):
    for c in flashed:
        data[c] = 0


def make_generation(data) -> int:
    # Increase all levels
    for c in data:
        data[c] += 1

    # Flash and spread
    flashed = []
    for c in data:
        if data[c] == 10 and c not in flashed:
            do_flash(data, c, flashed)

    reset_flashers(data, flashed)
    return len(flashed)


@timeit
def star1(data):
    days = 100
    res = sum(make_generation(data) for _ in range(days))
    print(res)


@timeit
def star2(data):
    datasize = maxx * maxy
    flashed, day = 0, 0
    while flashed != datasize:
        day += 1
        flashed = make_generation(data)
        printgrid(data, day)
    print(day)


star1(parse_data(data))
star2(parse_data(data))
