import json
import os

runtest = False
stardate = "14"
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Cell():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def line_to(self, c):
        res = []
        for x in range(min([self.x, c.x]), max([self.x, c.x]) + 1):
            for y in range(min([self.y, c.y]), max([self.y, c.y]) + 1):
                res.append(Cell(x, y))
        return res

    def down(self):
        return Cell(self.x, self.y + 1)

    def downleft(self):
        return Cell(self.x-1, self.y+1)

    def downright(self):
        return Cell(self.x+1, self.y+1)


class Cave():
    def __init__(self, data) -> None:
        self.cells = set()
        self.sand = set()

        for _ in data:
            segments = list(map(str.strip, _.split("->")))
            for i in range(len(segments)-1):
                start = Cell(*list(map(int, segments[i].split(","))))
                end = Cell(*list(map(int, segments[i+1].split(","))))
                for c in start.line_to(end):
                    self.add_cell(c)

    def add_cell(self, cell: Cell):
        self.cells.add(cell)

    def bottom(self) -> int:
        return max([_.y for _ in self.cells])

    def empty(self, cell):
        return cell not in self.cells and cell not in self.sand

    def drop_sand(self):
        bottom = self.bottom()
        sand = Cell(500, 0)
        while self.empty(sand) and sand.y < bottom:
            if self.empty(sand.down()):
                sand.y += 1
            elif self.empty(sand.downleft()):
                sand.x -= 1
                sand.y += 1
            elif self.empty(sand.downright()):
                sand.x += 1
                sand.y += 1
            else:
                self.sand.add(sand)
                break
        # print(sand,  len(self.sand))
        return sand.y == bottom or sand.y == 0


def star1():
    cave = Cave(data)
    cave_full = False
    while not cave_full:
        cave_full = cave.drop_sand()

    return len(cave.sand)


def star2():
    cave = Cave(data)
    bottom = cave.bottom() + 2
    bottomleft = Cell(500 - bottom - 1, bottom)
    bottomright = Cell(500 + bottom + 1, bottom)
    for c in bottomleft.line_to(bottomright):
        cave.add_cell(c)
    cave_full = False

    while not cave_full:
        cave_full = cave.drop_sand()

    return len(cave.sand)


print("star1:", star1())
print("star2:", star2())
