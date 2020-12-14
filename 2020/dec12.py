import os
import itertools
from timing import timeit
from pprint import pprint
import enum

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
# "F10",
# "N3",
# "F7",
# "R90",
# "F11",
# ]

class Instruction():
    def __init__(self, s):
        self.instr = s[0]
        self.value = int(s[1:])

    def __str__(self):
        return f"{self.instr}:{self.value:>3}"

class Direction(enum.Enum):
    EAST = 90
    SOUTH = 180
    WEST = 270
    NORTH = 0

class Ship:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.direction = Direction.EAST

    def traveldist(self):
        return abs(self.posX) + abs(self.posY)


class Ship1(Ship):
    def __init__(self):
        super().__init__()

    def move(self, instruction):
        if instruction.instr in 'NESWF':
            self.transport(instruction)
        elif instruction.instr in 'LR':
            self.turn(instruction)
        else:
            raise Exception(f"Unknown instruction {instruction.instr}")
        # print(f"{self.posX}/{self.posY} -> {self.direction}")

    def turn(self, instruction):
        turns = {'L': -1, 'R': 1}
        turn = turns[instruction.instr] * instruction.value
        d = (self.direction.value + turn) % 360
        self.direction = Direction(d)

    def transport(self, instruction):
        val = instruction.value
        ins = instruction.instr

        if ins in "FR":
            val *= {"F": 1, "R": -1}[ins]
            ins = self.direction.name[0]

        if ins == "N":
            self.posY += val
        elif ins == "S":
            self.posY -= val
        elif ins == "E":
            self.posX += val
        elif ins == "W":
            self.posX -= val

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def move(self, instruction):
        heading_value = {"N": 1, "S": -1, "E": 1, "W": -1}
        if instruction.instr in "NS":
            self.y += instruction.value * heading_value[instruction.instr]
        elif instruction.instr in "EW":
            self.x += instruction.value * heading_value[instruction.instr]
        else:
            raise Exception(f"Unknown move {instruction}")

    def turn(self, ins):
        rot = ins.value
        if rot == 270:
            rot = 90
            if ins.instr == "L":
                ins.instr = "R"
            else:
                ins.instr = "L"
        if rot == 180:
            self.x = -self.x
            self.y = -self.y
            return

        if rot == 90 and ins.instr == 'L':
            oldx = self.x
            self.x = -self.y
            self.y = oldx
            return

        if rot == 90 and ins.instr == 'R':
            oldx = self.x
            self.x = self.y
            self.y = -oldx
            return

        raise Exception("unhandled")

class Ship2(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint = Coord(10, 1)

    def move(self, instruction):
        oldx = self.posX
        oldy = self.posY
        if instruction.instr in 'NESW':
            self.waypoint.move(instruction)
        elif instruction.instr in 'LR':
            self.waypoint.turn(instruction)
        elif instruction.instr == "F":
            self.moveship(instruction)
        else:
            raise Exception(f"Unknown instruction {instruction}")
        # print(f"{instruction}: {oldx}/{oldy} --> {self.posX}/{self.posY} -- {self.waypoint}")

    def moveship(self, ins):
        self.posX += self.waypoint.x * ins.value
        self.posY += self.waypoint.y * ins.value

data = [Instruction(_) for _ in data]

def star1():
    ship = Ship1()
    for instr in data:
        ship.move(instr)

    print(f"* {ship.traveldist()}")

def star2():
    ship = Ship2()
    # ship.move(Instruction("R270"))
    # return
    c = 0
    for instr in data:
        c += 1
        ship.move(instr)
        # if c == 10:
        #     break

    print(f"** {ship.traveldist()}")

star1()
star2()