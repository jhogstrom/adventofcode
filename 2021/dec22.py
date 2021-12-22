import os
from typing import Dict, Tuple
from timer import timeit
from collections import defaultdict, deque

stardate = 22
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
# dataname = f"dec{stardate}_ex1.txt"
# dataname = f"dec{stardate}_ex2.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")

class Instruction():
    def parse_coords(self, s):
        _, coords = s.split("=")
        return [int(_) for _ in coords.split("..")]

    def __init__(self, s: str) -> None:
        command, coords = s.split()
        self.command = command == "on"
        self.coords = []

        for d in range(3):
            self.coords.append(self.parse_coords(coords.split(",")[d]))

    def __str__(self) -> str:
        switchmap = {True: "on", False: "off"}
        dims = "xyz"
        ranges = []
        for d in range(3):
            ranges.append(f"{dims[d]}={self.coords[d][0]}..{self.coords[d][1]}")
        return f"{switchmap[self.command]} {','.join(ranges)}"

    def n_range(self, d):
        _from = max([self.coords[d][0], -50])
        _to = min([self.coords[d][1], 50])
        return range(_from, _to+1)

    def xrange(self):
        return self.n_range(0)

    def yrange(self):
        return self.n_range(1)

    def zrange(self):
        return self.n_range(2)

    def toggle(self, cube: Dict[Tuple, bool]):
        for x in self.xrange():
            for y in self.yrange():
                for z in self.zrange():
                    if cube[(x,y,z)] == (not self.command):
                        # print(f"{(x, y, z)}: {cube[(x, y, z)]} => {self.command}")
                        cube[(x, y, z)] = self.command
        # print("Count:", sum(1 for _ in cube if cube[_]), "\n\n")


@timeit
def star1(data):
    instructions = [Instruction(_) for _ in data]
    cube = defaultdict(bool)
    for i in instructions:
        i.toggle(cube)

    print(sum(1 for _ in cube if cube[_]))


@timeit
def star2(data):
    ...

data2 = data[:]
star1(data)
star2(data2)