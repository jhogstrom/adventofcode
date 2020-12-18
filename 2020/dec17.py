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

class Space:
    def __init__(self, data, dimensions):
        self.dimensions = dimensions
        self.space = defaultdict(bool)
        self.gens = 0
        self.extremes = [(0, 0)] * self.dimensions
        self.parse(data)

    def parse(self, data):
        arr = {}
        zerodims = [0] * (self.dimensions - 2)
        for y in range(len(data)):
            for x in range(len(data[y])):
                arr[(x, y, *zerodims)] = data[y][x] == "#"
        self.update_space(arr)

    def print(self):
        print(f"After {self.gens} cycles:")
        charmap = {True: '#', False: '.'}

        zr = range(self.extremes[2][0], self.extremes[2][1]+1)
        yr = range(self.extremes[1][0], self.extremes[1][1]+1)
        xr = range(self.extremes[0][0], self.extremes[0][1]+1)

        for z in zr:
            print(f"z={z}")
            for y in yr:
                print(''.join([charmap[self.space[(x, y, z)]] for x in xr]))
            print()

    def update_space(self, arr):
        self.space = defaultdict(bool, {k:v for k,v in arr.items() if v})

        for d in range(self.dimensions):
            values = [_[d] for _ in self.space] or [0]
            self.extremes[d] = (min(values), max(values))

    def neighbours(self, c):
        ranges = [(c[d]-1, c[d], c[d]+1) for d in range(self.dimensions)]
        coords = [_ for _ in itertools.product(*ranges) if _ != c]

        return len([_ for _ in coords if self.space[_]])

    def cycle(self):
        self.gens += 1
        # print(f"{self.gens}")
        nextgen = {}
        ranges = [range(self.extremes[d][0]-1, self.extremes[d][1]+2) \
                    for d in range(self.dimensions)]

        for coord in itertools.product(*ranges):
            n = self.neighbours(coord)
            if self.space[coord]:
                nextgen[coord] = n in [2, 3]
            else:
                nextgen[coord] = n == 3

        self.update_space(nextgen)

    def count(self):
        return len([_ for _ in self.space.values()])


@timeit
def cycle_game(dimensions):
    space = Space(data, dimensions)
    for c in range(6):
        space.cycle()
        # print("count:", space.count())
    return space.count()


print(f"* {cycle_game(3)}")
print(f"** {cycle_game(4)}")
