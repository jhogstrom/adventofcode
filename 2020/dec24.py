import helpers
from enum import Enum, auto
from collections import defaultdict

extra = "_demo"
extra = ""
data = helpers.get_data(__file__, extra=extra)


class Direction(Enum):
    e = auto()
    se = auto()
    sw = auto()
    w = auto()
    nw  = auto()
    ne = auto()

def parse(data):
    dirs = [name for name, member in Direction.__members__.items()]
    res = []
    for s in data:
        line = []
        while s:
            d = 1
            while s[:d] not in dirs:
                d += 1
            line.append(s[:d])
            s = s[d:]
        res.append(line)
    return res

def move(p, d):
    if d == "e":
        return ((p[0]+2, p[1]))
    if d == "se":
        return ((p[0]+1, p[1]-1))
    if d == "sw":
        return ((p[0]-1, p[1]-1))

    if d == "w":
        return ((p[0]-2, p[1]))
    if d == "nw":
        return ((p[0]-1, p[1]+1))
    if d == "ne":
        return ((p[0]+1, p[1]+1))

def gridcount(grid):
    return len([v for v in grid.values() if v])

def star1():
    grid = defaultdict(bool)
    instr = parse(data)
    for line in instr:
        p = (0, 0)
        for i in line:
            p = move(p, i)
        grid[p] = not grid[p]

    res = gridcount(grid)
    return res, grid

def neighbors(cells, grid):
    return len([_ for _ in cells if grid.get(_, False)])


def get_neighbors(p):
    dirs = [name for name, member in Direction.__members__.items()]
    res = set()
    for d in dirs:
        pn = move(p, d)
        res.add(pn)
    return res


def star2(grid):
    # print(f"Day 0: {gridcount(grid)}")

    for d in range(100):
        n_cells = set()
        nextgrid = {}
        for p in grid:
            # print(p)
            adjacent = get_neighbors(p)
            n = neighbors(adjacent, grid)
            n_cells |= adjacent

            if grid[p] and (n == 0 or n > 2):
                nextgrid[p] = False
            elif not grid[p] and n == 2:
                nextgrid[p] = True
            else:
                nextgrid[p] = grid[p]
            # print(f"{str(p):10} {n} {grid[p]:2} => {nextgrid[p]:2}")

        # Now check all neighbors not yet checked
        knowncells = nextgrid.keys()
        for np in [_ for _ in n_cells if _ not in knowncells]:
            n = neighbors(get_neighbors(np), grid)

            if (n == 0 or n > 2) and grid[np]:
                nextgrid[np] = False
            elif n == 2 and not grid[np]:
                nextgrid[np] = True
            else:
                nextgrid[np] = grid[np]



        grid = defaultdict(bool, {k:v for k, v in nextgrid.items() if v})
        # print(f"Day {d+1}: {gridcount(grid)}")
    return gridcount(grid)


s1, grid = star1()
print(f"* {s1}")
print(f"** {star2(grid)}")

