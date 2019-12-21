from computer import intcomputer
from cell import Cell
import os
from time import sleep

class Robot:
    def __init__(self, intcode = None):
        prg = self.get_prg()
        if not intcode is None:
            prg[0] = intcode
        self.c = intcomputer(prg, param_array=[])
        self.grid = []
        self.alignments = []

    def get_prg(self):
        curdir = os.path.dirname(os.path.abspath(__file__))
        filename = f'{curdir}\\dec17.txt'
        return [int(_) for _ in open(filename, 'r').readline().split(",")]

    def harvest_grid(self):
        self.grid = []
        s = ""
        for a in self.c.outputarray:
            if int(a) == 10:
                self.grid.append(s)
                s = ""
                continue
            c = chr(int(a))
            s += c
        self.c.outputarray = []
        return

        self.grid = ["..#..........",
                     "..#..........",
                     "##O####...###",
                     "#.#...#...#.#",
                     "##O###O###O##",
                     "..#...#...#..",
                     "..#####...^.."]


    def make_scaffolding(self):
        self.c.execute()
        self.harvest_grid()

    def makeintcode(self, s):
        return [ord(_) for _ in s+"\n"]

    def addroutine(self, s):
        self.c.input += self.makeintcode(s)

    def videostream(self, video):
        videostream = {True: "y", False: "n"}
        self.c.input += self.makeintcode(videostream[video])

    def crawl(self):
        while not self.c._terminated:
            self.c.execute()
            self.harvest_grid()
            self.print_grid(zoom=False)
            sleep(1)

    def print_grid(self, zoom=False):
        if not zoom:
            for s in self.grid:
                print(s)
        else:
            ROBOTPOS = "v^<>X"
            for i in range(len(self.grid)-1,0,-1):
                if any([_ in self.grid[i] for _ in ROBOTPOS]):
                    r = i
                    break

            for s in self.grid[max(0, r-3):r+3]:
                print(s)


        print("==")

    def char(self, x, y):
        return self.grid[y][x]

    def ischar(self, x, y, c):
        return self.char(x, y) == c

    def iscross(self, x, y):
        return  self.ischar(x-1, y, "#") and \
                self.ischar(x+1, y, "#") and \
                self.ischar(x, y-1, "#") and \
                self.ischar(x, y+1, "#") and \
                self.ischar(x, y, "#")

    def find_alignments(self):        
        for y in range(1, len(self.grid)-1):
            for x in range(1, len(self.grid[y])-1):
                if self.iscross(x, y):
                    self.alignments.append(Cell(x, y))


def dec17_star1():
    r = Robot()
    r.make_scaffolding()
    r.print_grid()
    r.find_alignments()
    answer = sum([_.x * _.y for _ in r.alignments])
    print(f"Answer: {answer}")

############

def dec17_star2():
    r = Robot(2)
    r.addroutine("A,B,C,A,A")
    r.addroutine("R,12,L,6")
    r.addroutine("5,L,10,L,7,L,12")
    r.addroutine("R,12,L,4,R,12,L,L\n")
    r.videostream(True)
    r.crawl()

#dec17_star1()

dec17_star2()
