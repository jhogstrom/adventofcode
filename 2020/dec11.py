import os
import itertools
from timing import timeit
from pprint import pprint

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
# "L.LL.LL.LL",
# "LLLLLLL.LL",
# "L.L.L..L..",
# "LLLL.LL.LL",
# "L.LL.LL.LL",
# "L.LLLLL.LL",
# "..L.L.....",
# "LLLLLLLLLL",
# "L.LLLLLL.L",
# "L.LLLLL.LL"
# ]

class FloorPlan():
    def __init__(self, data):
        self.data = data.copy()
        self.maxx = len(data[0])
        self.maxy = len(data)
        self.directions = (
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1))


    def occupied1(self, x, y) -> int:
        if x < 0 or x >= len(self.data[0]):
            return 0
        if y < 0 or y >= len(self.data):
            return 0
        return int(self.data[y][x] == "#")

    def neighbours(self, x, y, maxval) -> int:
        c = 0
        for i, d in enumerate(self.directions):
            c += self.occupied1(x + d[0], y + d[1])
            if c > maxval:
                return c
            if len(self.directions) - i < maxval - c:
                return c
        return c

    def occupied2(self, x, y, dx, dy) -> int:
        while True:
            x += dx
            y += dy
            if x < 0 or x == self.maxx or y < 0 or y == self.maxy:
                return False
            # print(x, y)
            c = self.data[y][x]
            if c in "L#":
                return int(c == "#")

        return 0

    def neighbours2(self, x, y, maxval) -> int:
        c = 0
        for i, d in enumerate(self.directions):
            c += self.occupied2(x, y, d[0], d[1])
            if c > maxval:
                return c
            if len(self.directions) - i < maxval - c:
                return c
        return c

    def makeround1(self):
        nextgen = []
        for y in range(len(self.data)):
            row = []
            for x in range(len(self.data[y])):
                cell = self.data[y][x]
                if cell == ".":
                    row.append(".")
                elif cell == "L":
                    if self.neighbours(x, y, 0) == 0:
                        row.append("#")
                    else:
                        row.append("L")
                else:
                    if self.neighbours(x, y, 4) >= 4:
                        row.append("L")
                    else:
                        row.append("#")
            nextgen.append("".join(row))
        self.data = nextgen.copy()

    def makeround2(self):
        nextgen = []
        for y in range(len(self.data)):
            row = []
            for x in range(len(self.data[y])):
                cell = self.data[y][x]
                if cell == ".":
                    row.append(".")
                elif cell == "L":
                    if self.neighbours2(x, y, 0) == 0:
                        row.append('#')
                    else:
                        row.append('L')
                else:
                    if self.neighbours2(x, y, 5) >= 5:
                        row.append('L')
                    else:
                        row.append('#')
            nextgen.append("".join(row))
        self.data = nextgen.copy()

    def print(self):
        for y in range(len(self.data)):
            print(self.data[y])
        print("---")

    def count(self):
        res = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                res += int(self.data[y][x] == "#")
        return res

    @timeit
    def star1(self):
        prevdata = []
        # c = 0
        while self.data != prevdata:
            # c += 1
            prevdata = self.data.copy()
            self.makeround1()
            # print(c)

    @timeit
    def star2(self):
        prevdata = []
        # c = 0
        while self.data != prevdata:
            # c += 1
            prevdata = self.data.copy()
            self.makeround2()
            # print(c)

def star1():
    floor = FloorPlan(data)
    floor.star1()
    print(f"* {floor.count()}")

def star2():
    floor = FloorPlan(data)
    floor.star2()
    print(f"** {floor.count()}")

star1()
star2()