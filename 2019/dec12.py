import os
from collections import defaultdict

curdir = os.path.dirname(os.path.abspath(__file__))

data = ["<x=19, y=-10, z=7>",
        "<x=1, y=2, z=-3>",
        "<x=14, y=-4, z=1>",
        "<x=8, y=7, z=-6>"]

#data = ["<x=-1, y=0, z=2>",
#        "<x=2, y=-10, z=-7>",
#        "<x=4, y=-8, z=8>",
#        "<x=3, y=5, z=-1>"]


class Cell3d:
    def __init__(self, s):
        s = [_.strip() for _ in s.replace("<", "").replace(">", "").split(",")]
        self.x = int(s[0].split("=")[1])
        self.y = int(s[1].split("=")[1])
        self.z = int(s[2].split("=")[1])
        self.vx = self.vy = self.vz = self.newvx = self.newvy = self.newvz = 0

    def __str__(self):
        #pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
        return f"pos=<x={self.x:>3}, y={self.y:>3}, z={self.z:>3}> vel=<x={self.vx:>3}, y={self.vy:>3}, z={self.vz:>3}>"

    def comparison(self, v1, v2):
        if v1 > v2:
            return -1
        if v1 < v2:
            return 1
        return 0

    def apply_gravity(self, c2):
        self.newvx += self.comparison(self.x, c2.x)
        self.newvy += self.comparison(self.y, c2.y)
        self.newvz += self.comparison(self.z, c2.z)

    def apply_speed(self):
        self.vx = self.newvx
        self.vy = self.newvy
        self.vz = self.newvz
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

def print_cells(cells, rounds):
    print(f"After {rounds} steps:")
    for c in cells:
        print(c)
    print()


def dec12_star1():
    states = defaultdict(list)
    deltas = {}
    cells = [Cell3d(_) for _ in data]
    print_cells(cells, 0)
    prev_te = sum([_.total_energy() for _ in cells])
    for i in range(1000):
        for c in cells:
            others = cells.copy()
            others.remove(c)
            for c2 in others:
                c.apply_gravity(c2)

        for c in cells:
            c.apply_speed()

        t_e = sum([_.total_energy() for _ in cells])
        diff = t_e - prev_te
#        print(f"{i:>4} - {t_e:>4} | {t_e - prev_te}")
        prev_te = t_e
        if diff in deltas:
            print(i, deltas[diff])
        deltas[diff] = i 
#        if t_e in states:
#            print_cells(cells)
#            for c in states[t_e]:
#                print_cells(c)

        



 #       print_cells(cells, i+1)
        
    for c in cells:
        print(f"{c.potential_energy()} {c.kinetic_energy()} => {c.total_energy()}")

    total_energy = sum([_.total_energy() for _ in cells])
    print(f"Total: {total_energy}")


dec12_star1()