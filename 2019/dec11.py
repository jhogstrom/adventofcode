from computer import intcomputer
from cell import Cell
import os
from collections import defaultdict
from time import sleep
import copy

curdir = os.path.dirname(os.path.abspath(__file__))


class Robot:
    def __init__(self, computer, grid=defaultdict(int)):
        self.directions = "URDL"
        self.direction = 0
        self.computer = computer
        self.grid = grid
        self.current_cell = Cell(0, 0)

    def turn(self, d):
        assert(d in [0, 1])
        turns = {0: 3, 1: 1}
        turns_names = {0: "Left", 1: "Right"}
        self.direction += turns[d]
        self.direction %= 4

    def __str__(self):
        res = []
        res.append(f"Current: {self.current_cell}")
        res.append(f"direction: {self.directions[self.direction]}")
        for c in self.grid:
            res.append(f"{c} - {self.grid[c]}")

        return str(res)

    def move(self):
        self.current_cell = self.current_cell.nextmove(self.directions[self.direction])

    def step(self):
        nextinput = self.grid[self.current_cell]
        self.computer.execute(p=nextinput)
        next_color = self.computer.pop_output()
        next_turn = self.computer.pop_output()

        self.grid[self.current_cell] = next_color
        self.turn(next_turn)
        self.move()

    def run(self):
        while not self.computer._terminated:
            self.step()

    def printtrack(self):
        miny = min([_.y for _ in self.grid])
        maxy = max([_.y for _ in self.grid])
        minx = min([_.x for _ in self.grid])
        maxx = max([_.x for _ in self.grid])

        pixelmap = {True: "x", False: " "}

        for y in range(maxy, miny-1, -1):
            s = ""
            for x in range(minx, maxx+1):
                c = Cell(x, y)
                print(pixelmap[c in self.grid and self.grid[c] > 0], end="")
            print()
        print("===")

cnt = 0
def dec11_star1():
    global cnt
    filename = f'{curdir}\\dec11.txt'
    prgdata = open(filename, 'r').readline()

    prg = [int(_) for _ in prgdata.split(",")]    
    computer = intcomputer(prg, name=f"PainterRobot{cnt}")
    
    cnt += 1
    robot = Robot(computer)
    robot.run()
    #print(len(robot.grid))
    print("DONE")

def dec11_star2():
    filename = f'{curdir}\\dec11.txt'
    prgdata = open(filename, 'r').readline()

    prg = [int(_) for _ in prgdata.split(",")]    
    startgrid = defaultdict(int)
    startgrid[Cell(0, 0)] = 1
    computer = intcomputer(prg, name=f"PainterRobot2")

    robot = Robot(computer, grid=startgrid)
    robot.run()
    robot.printtrack()
    print(len(robot.grid))
    print("DONE")


#c = intcomputer("", name="foo")
#d = intcomputer("", name="foo")

dec11_star1()
dec11_star1()
#dec11_star2()
#dec11_star2()
