from computer import intcomputer
from cell import Cell
import os
from time import sleep
from collections import defaultdict

class Myqueue:
    def __init__(self):
        self.keylist = []
        self.datalist = []

    def add(self, key, data):
        self.keylist.append(key)
        self.datalist.append(data)

    def ensurekey(self, key, data):
        if self.contains(key):
            return
        self.add(key, data)

    def pop(self):
        data = self.datalist[-1]
        key = self.keylist[-1]
        self.datalist = self.datalist[:-1]
        self.keylist = self.keylist[:-1]
        return key, data

    def contains(self, key):
        return key in self.keylist

    def dataforkey(self, key):
        ix = self.keylist.index(key)
        return self.datalist[ix]

    def peek_key(self):
        return self.keylist[-1]

    def peek_data(self):
        return self.datalist[-1]





class Labyrinth:
    def __init__(self):
        self.DIRECTION = [1, 4, 2, 3] # N E S W
        self.MOVES = {
                1: Cell(0, 1),  # N
                4: Cell(1, 0),  # E
                2: Cell(0, -1), # S
                3: Cell(-1, 0)} # W
        self.current_cell = Cell(0, 0)
        self.current_direction = 0
#        self.trail = defaultdict(list)
##        self.trail[self.current_cell] = [self.current_direction]
        self.trail = Myqueue()
        self.grid = {}
        self.grid[self.current_cell] = "."

        prgdata = self.get_prg()
        self.c = intcomputer(prgdata, param_array=[])

    def get_prg(self):
        curdir = os.path.dirname(os.path.abspath(__file__))
        filename = f'{curdir}\\dec15.txt'
        return [int(_) for _ in open(filename, 'r').readline().split(",")]

    def get_result(self, direction):
        return self.c.execute(direction).pop_output()

    def backtrack(self):
        print(f"Current cell: {self.current_cell} => {self.current_direction} // {self.trail.peek_data()}")
        self.trail.pop()
        self.current_cell = self.trail.peek_key()
        self.current_direction = self.trail.dataforkey(self.current_cell)[-1]
        print(f"Backtracked : {self.current_cell} => {self.current_direction} // {self.trail.peek_data()}")

        #raise Exception("Backtracking")

    def step(self):
        # Check where next move takes us

        nextcell = self.current_cell.add(
            self.MOVES[self.DIRECTION[self.current_direction]].x, 
            self.MOVES[self.DIRECTION[self.current_direction]].y)

        while nextcell in self.grid or self.trail.contains(nextcell):
            self.trail.dataforkey(self.current_cell).append(self.current_direction)
            self.current_direction += 1
            self.current_direction %= 4
            nextcell = self.current_cell.add(
                self.MOVES[self.DIRECTION[self.current_direction]].x, 
                self.MOVES[self.DIRECTION[self.current_direction]].y)


        # If we backtrack, then turn again (in next step)
#        if self.trail.contains(nextcell):
#            self.current_direction += 1
#            self.current_direction %= 4
#            self.trail.dataforkey(nextcell).append(self.current_direction)
#            return

        # Check the result of the move
        moveresult = self.get_result(self.DIRECTION[self.current_direction])

        # Unable to move - we hit a wall
        if moveresult == 0:            
            # Mark the grid with wall
            self.grid[nextcell] = "#"
            # Remember where we headed last on this spot
            self.trail.ensurekey(self.current_cell, [])
            self.trail.dataforkey(self.current_cell).append(self.current_direction)

            if len(self.trail.dataforkey(self.current_cell)) == 4:
                self.backtrack()
                sleep(1)
                return False

            # Turn clock-wise for next step
            self.current_direction += 1
            self.current_direction %= 4

            return False

        # We could progress!
        if moveresult == 1:
            # Mark the grid with free space
            self.grid[nextcell] = "."
            # Mark the current cell that we tried this direction
            self.trail.dataforkey(self.current_cell).append(self.current_direction)
            # No need trying the back direction.
            self.trail.ensurekey(nextcell, [])
            self.trail.dataforkey(nextcell).append((self.current_direction + 2) % 4)
            # Move to the next cell
            self.current_cell = nextcell
            # Start by looking north
            self.current_direction = 0

            return False

        self.grid[nextcell] = "O"
        return True
            
    def step2(self):
        # Check where next move takes us

        nextcell = self.current_cell.add(
            self.MOVES[self.DIRECTION[self.current_direction]].x, 
            self.MOVES[self.DIRECTION[self.current_direction]].y)

        while nextcell in self.grid or self.trail.contains(nextcell):
            self.trail.dataforkey(self.current_cell).append(self.current_direction)
            self.current_direction += 1
            self.current_direction %= 4
            nextcell = self.current_cell.add(
                self.MOVES[self.DIRECTION[self.current_direction]].x, 
                self.MOVES[self.DIRECTION[self.current_direction]].y)


        # If we backtrack, then turn again (in next step)
#        if self.trail.contains(nextcell):
#            self.current_direction += 1
#            self.current_direction %= 4
#            self.trail.dataforkey(nextcell).append(self.current_direction)
#            return

        # Check the result of the move
        moveresult = self.get_result(self.DIRECTION[self.current_direction])

        # Unable to move - we hit a wall
        if moveresult == 0:            
            # Mark the grid with wall
            self.grid[nextcell] = "#"
            # Remember where we headed last on this spot
            self.trail.ensurekey(self.current_cell, [])
            self.trail.dataforkey(self.current_cell).append(self.current_direction)

            if len(self.trail.dataforkey(self.current_cell)) == 4:
                self.backtrack()
                sleep(1)
                return False

            # Turn clock-wise for next step
            self.current_direction += 1
            self.current_direction %= 4

            return False

        # We could progress!
        if moveresult == 1:
            # Mark the grid with free space
            self.grid[nextcell] = "."
            # Mark the current cell that we tried this direction
            self.trail.dataforkey(self.current_cell).append(self.current_direction)
            # No need trying the back direction.
            self.trail.ensurekey(nextcell, [])
            self.trail.dataforkey(nextcell).append((self.current_direction + 2) % 4)
            # Move to the next cell
            self.current_cell = nextcell
            # Start by looking north
            self.current_direction = 0

            return False

        self.grid[nextcell] = "O"
        return True

    def print(self):
        miny = min([_.y for _ in self.grid])
        maxy = max([_.y for _ in self.grid])
        minx = min([_.x for _ in self.grid])
        maxx = max([_.x for _ in self.grid])

        pixelmap = {True: "x", False: " "}

        for y in range(maxy, miny-1, -1):
            for x in range(minx, maxx+1):
                c = Cell(x, y)
                if c in self.grid:
                    print(self.grid[c], end="")
                else:
                    print(" ", end="")
            print()
        print("==")

def dec15_star1():
    labyrinth = Labyrinth()
    while not labyrinth.step():
        labyrinth.print()
        sleep(0.1)

dec15_star1()