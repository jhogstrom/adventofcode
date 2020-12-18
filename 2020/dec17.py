import os
import itertools
from timing import timeit
import enum
from collections import defaultdict

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
# ".#.",
# "..#",
# "###",
# ]

class Coord:
    def __init__(self, x, y, z):
        self.coords = (x, y, z)
        self.x = x
        self.y = y
        self.z = z
        self.active = True

    def __eq__(self, other):
        return self.coords == other.coords

    def __str__(self):
        s = [str(_) for _ in self.coords]
        return f"Cell: ({', '.join(s)})"

class Space:
    def __init__(self, data):
        # self.space = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))
        self.dimensions = 3
        self.space = []
        self.gens = 0
        self.extremes = [(0, 0)] * self.dimensions
        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0
        self.minz = 0
        self.maxz = 0
        self.parse(data)


    def get_cell(self, x, y, z):
        c = Coord(x, y, z)
        try:
            i = self.space.index(c)
            return c
        except:
            c.active = False
            return c

    def parse(self, data):
        arr = []
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == "#":
                    arr.append(Coord(x, y, 0))
        self.update_space(arr)

    def print(self):
        print(f"After {self.gens} cycles:")
        charmap = {True: '#', False: '.'}

        for z in range(self.minz, self.maxz + 1):
            print(f"z={z}")
            for y in range(self.miny, self.maxy+1):
                print(''.join([charmap[self.get_cell(x, y, z).active] for x in range(self.minx, self.maxx+1)]))
            print()

    def update_space(self, arr):
        self.space = arr

        for d in range(self.dimensions):
            values = [_.coords[d] for _ in arr]
            self.extremes[d] = (min(values), max(values))

        self.minx = min([_.x for _ in arr])
        self.maxx = max([_.x for _ in arr])
        self.miny = min([_.y for _ in arr])
        self.maxy = max([_.y for _ in arr])
        self.minz = min([_.z for _ in arr])
        self.maxz = max([_.z for _ in arr])

    def neighbours(self, c):
        # print(c)
        coords = [_ for _ in itertools.product(
            [c.x-1, c.x, c.x+1],
            [c.y-1, c.y, c.y+1],
            [c.z-1, c.z, c.z+1]) if _ != c.coords]

        neighbours = [_ for _ in self.space if (_.x, _.y, _.z) in coords]
        return len(neighbours)


    def cycle(self):
        self.gens += 1
        nextgen = []
        # for x in range(self.minx-1, self.maxx+2):
        #     for y in range(self.miny-1, self.maxy+2):
        #         for z in range(self.minz-1, self.maxz+2):
        ranges = []
        for d in range(self.dimensions):
            ranges.append(range(self.extremes[d][0]-1, self.extremes[d][1]+2))
        for coord in itertools.product(*ranges):
            # print(coord)
            x = coord[0]
            y = coord[1]
            z = coord[2]
            c = self.get_cell(x, y, z)
            n = self.neighbours(c)
            if c.active:
                if n in [2, 3]:
                    nextgen.append(c)
            else:
                if n == 3:
                    nextgen.append(Coord(c.x, c.y, c.z))

        self.update_space(nextgen)

    def count(self):
        return len([_ for _ in self.space if _.active])

# print(len(list(itertools.product([1, 2, 3], ['A', 'B', 'C'], ['x', 'y', 'z']))))
# print(list(itertools.product(range(1,3), ['a', 'b'])))
# exit()

# ranges = []
# for d in range(3):
#     ranges.append(range(0, 3))
# print(ranges)
# for coord in itertools.product(*ranges):
#     print(coord)
# exit()

space = Space(data)
space.print()

for c in range(6):
    space.cycle()
    # space.print()
print(space.count())

