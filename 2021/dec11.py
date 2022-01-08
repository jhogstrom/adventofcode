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


d = []
for r in data:
    d.append([int(_) for _ in r])
data = d


def printgrid(data, flashes, gen):
    print(f"===After step {gen}:")
    for r in data:
        print(" ".join(str(_) for _ in r))
    print(f"FLASHES: {flashes}")


class Coord():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def neighbors(self):
        return [
            Coord(self.x-1, self.y-1),
            Coord(self.x, self.y-1),
            Coord(self.x+1, self.y-1),
            Coord(self.x-1, self.y),
            Coord(self.x+1, self.y),
            Coord(self.x-1, self.y+1),
            Coord(self.x, self.y+1),
            Coord(self.x+1, self.y+1),
            ]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y


def inboard(data, coord: Coord) -> bool:
    return coord.x >= 0 and coord.x < len(data[0]) and coord.y >= 0 and coord.y < len(data)

flashed = []

def do_flash(data, coord: Coord, sender: Coord):
    # print(f"{sender} Flashing {coord}")
    flashed.append(coord)
    neighbors = coord.neighbors()
    for n in neighbors:
        if inboard(data, n):
            data[n.y][n.x] += 1
            # print(f"{n} -> {data[n.y][n.x]} -> {data[n.y][n.x] > 9}")
            if data[n.y][n.x] > 9 and n not in flashed:
                do_flash(data, n, coord)


def reset_flashers(data):
    res = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] > 9:
                data[y][x] = 0
                res += 1
    return res


def make_generation(data):
    global flashed
    flashed = []
    # Increase all levels
    for y in range(len(data)):
        for x in range(len(data[y])):
            data[y][x] += 1


    # Flash and spread
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == 10:
                c = Coord(x, y)
                if c not in flashed:
                    do_flash(data, c, c)

    res = reset_flashers(data)
    return res


@timeit
def star1(data):
    totalsteps = 100
    res = 0
    # printgrid(data, res, 0)
    for c in range(totalsteps):
        res += make_generation(data)

    print(res)


@timeit
def star2(data):
    datasize = len(data) * len(data[0])
    totalsteps = 200000
    # printgrid(data, res, 0)
    for c in range(totalsteps):
        r = make_generation(data)
        # printgrid(data, res, c+1)
        if r == datasize:
            print(c+1)
            return


data2 = data[:]
star1(data)
star2(data2)