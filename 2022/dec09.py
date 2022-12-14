import os
from typing import List

runtest = False
stardate = "09"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()

# data = [  # NOSONAR
#     "R 5",
#     "U 8",
#     "L 8",
#     "D 3",
#     "R 17",
#     "D 10",
#     "L 25",
#     "U 20"
# ]


class Coord:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def move(self, coord):
        self.x += coord.x
        self.y += coord.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def adjust(self, other):
        deltax = other.x - self.x
        deltay = other.y - self.y
        dx = 0
        dy = 0

        if [abs(deltax), abs(deltay)] == [2, 2]:
            dx = deltax // 2
            dy = deltay // 2
        elif abs(deltax) == 2:
            dx = deltax // 2
            dy = deltay
        elif abs(deltay) == 2:
            dx = deltax
            dy = deltay // 2
        if max([abs(deltax), abs(deltay)]) > 2:
            raise ValueError(deltax, deltay)
        self.x += dx
        self.y += dy
        # print(f"adjusted for {deltax}, {deltay} with {dx}, {dy}")


class Rope():
    def __init__(self, ropelength: int) -> None:
        self.knots: List[Coord] = []
        for _ in range(ropelength):
            self.knots.append(Coord(0, 0))
        self.tvisited = set()
        self.trail = []

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def make_move(self, move):
        moves = {
            'U': Coord(0, 1),
            'D': Coord(0, -1),
            'L': Coord(-1, 0),
            'R': Coord(1, 0)
        }
        self.trail.append(move)
        m, count = move.split()
        for _ in range(int(count)):
            self.head.move(moves[m])
            for i, k in enumerate(self.knots[1:], 1):
                try:
                    self.knots[i].adjust(self.knots[i-1])
                    # self.print(f"{move} #{_} (knot {i})")
                except ValueError:
                    print("-->", move)
                    self.print()
                    raise
            self.tvisited.add(str(self.tail))
            self.trail.append(str(self.tail))

            # print(move, moves[m], self.head, len(self.tvisited))

    def print(self, s: str = None):  # NOSONAR
        lines = []
        rope = [str(_) for _ in self.knots]
        x = [_.x for _ in self.knots]
        y = [_.y for _ in self.knots]
        print(s or "")
        for _y in range(min(y)-1, max(y)+2):
            s = ""
            for _x in range(min(x)-1, max(x)+2):
                c = str(Coord(_x, _y))
                ch = "#"

                for i, _ in enumerate(self.knots[1:], 1):
                    if c == str(_):
                        ch = str(i)
                if c == str(self.head):
                    ch = "H"
                s += ch if c in rope else "."
            lines.append(s)

        for i, _ in enumerate(lines[::-1], -1):
            print(f"{max(y)-i:>4}  {_}")

        print(", ".join([str(_) for _ in self.knots]))


def solve(n):
    rope = Rope(n)
    for _ in data:
        rope.make_move(_)
        # rope.print(_)
    return len(rope.tvisited)


def star1():
    return solve(2)


def star2():
    return solve(10)


print("star1", star1())
print("star2", star2())
