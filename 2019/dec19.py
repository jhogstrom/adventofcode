from computer import intcomputer
from cell import Cell
import os
from time import sleep

class Scanner:
    def __init__(self):
        filename = __file__.replace(".py", ".txt")
        self.prg = [int(_) for _ in open(filename, 'r').readline().split(",")]


    def get_beam(self, x, y):
        return intcomputer(self.prg.copy(), param_array=[x, y], debug=False).execute().pop_output()

    def fit_ship(self, x, y):
        return self.get_beam(x, y-99) == 1 and self.get_beam(x+99, y-99) == 1

    def find_ship(self):
        startpos = {}
        y = 100
        x = 0
        while True:
            if y-1 in startpos:
                x = startpos[y-1]
            while self.get_beam(x, y) == 0:
                x += 1
            startpos[y] = x

            if y % 100 == 0:
                print(f"{y:>3}: {x:>3}")
            
            if self.fit_ship(x, y):
                print(f"Answer: {x*10000 + y-99}")
                return
            y += 1


def dec19_star1():
    scanner = Scanner()
    s = 0
    for y in range(50):
        for x in range(50):
            s += scanner.get_beam(x, y)

    print(f"Answer: {s}")


def dec19_star2():
    scanner=Scanner()
    scanner.find_ship()

dec19_star2()

