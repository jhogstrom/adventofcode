from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "21"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def neighbors(p):
    x, y = p
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def print_grid(grid, pos):
    maxx = max([x for x, _ in grid.keys()])
    maxy = max([y for _, y in grid.keys()])
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) in pos:
                print("O", end="")
            else:
                print(grid[(x, y)], end="")
        print()
    print("===")


@timeit
def star1(data):
    logging.debug("running star 1")
    grid = {}
    pos = set()
    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]
            if c == "S":
                pos.add((x, y))
                c = "."
            grid[(x, y)] = c

    STEPS = 64
    for _ in range(STEPS):
        newpos = set()
        for p in pos:
            for n in neighbors(p):
                if grid.get(n) == ".":
                    newpos.add(n)
        pos = newpos
    print(len(pos))

@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
