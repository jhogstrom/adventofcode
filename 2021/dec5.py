import os
from timer import timeit
from collections import defaultdict

stardate = 5
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]


class Coord():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"


class CoordFromLine(Coord):
    def __init__(self, s) -> None:
        x, y = s.split(",")
        super().__init__(int(x), int(y))


class Line():
    def __init__(self, c1: Coord, c2: Coord) -> None:
        self.start = c1
        self.end = c2

    def isHorizontal(self):
        return self.start.x == self.end.x

    def isVertical(self):
        return self.start.y == self.end.y

    def isDiagonal(self):
        h = self.start.x - self.end.x
        v = self.start.y - self.end.y
        return abs(h) == abs(v)

    def span(self):
        res = []
        if self.isVertical():
            line_ends = [self.start.x, self.end.x]
            for x in range(min(line_ends), max(line_ends) + 1):
                res.append(Coord(x, self.start.y))

        if self.isHorizontal():
            line_ends = [self.start.y, self.end.y]
            for y in range(min(line_ends), max(line_ends) + 1):
                res.append(Coord(self.start.x, y))

        if self.isDiagonal():
            deltax = 0
            if self.start.y > self.end.y and self.start.x < self.end.x:  # SW -> NE /^
                dx = 1
                dy = -1
                yrange = range(self.start.y, self.end.y - 1, dy)

            if self.start.y > self.end.y and self.start.x > self.end.x:  # SE -> NW v\
                dx = -1
                dy = -1
                yrange = range(self.start.y, self.end.y - 1, dy)

            if self.start.y < self.end.y and self.start.x < self.end.x:  # NW -> SE \v
                dx = 1
                dy = 1
                yrange = range(self.start.y, self.end.y + 1, dy)

            if self.start.y < self.end.y and self.start.x > self.end.x:  # NE -> SW v/
                dx = -1
                dy = 1
                yrange = range(self.start.y, self.end.y + 1, dy)

            for y in yrange:
                res.append(Coord(self.start.x + deltax, y))
                deltax += dx

        return res

    def __str__(self) -> str:
        return f"{self.start} -> {self.end}"


def parse(line):
    c1, _, c2 = line.split()
    return CoordFromLine(c1), CoordFromLine(c2)


def printgrid(d: dict):
    maxsize_x = max(_[0] for _ in d)
    maxsize_y = max(_[1] for _ in d)
    maxsize_x = maxsize_y = 13
    for y in range(maxsize_y):
        for x in range(maxsize_x):
            v = d[(x, y)]
            if v == 0: v = "."
            print(f" {v}", end="")
        print()


def dowork(data, includeDiagonal):
    grid = []
    for row in data:
        l = Line(*parse(row))

        if l.isHorizontal() or l.isVertical() or (includeDiagonal and l.isDiagonal()):
            grid.extend(l.span())

    counter = defaultdict(int)
    for c in grid:
        counter[(c.x, c.y)] += 1
    printgrid(counter)

    # Count all coordinates hit by more than 1 line.
    print(sum(1 for _ in counter.values() if _ > 1))


@timeit
def star1(data):
    dowork(data, False)

@timeit
def star2(data):
    dowork(data, True)

star1(data)
star2(data)