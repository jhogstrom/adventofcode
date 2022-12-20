import os

runtest = False
stardate = 18
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Coord():
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def neighbors(self):
        return [
            (self.x, self.y-1, self.z), (self.x, self.y+1, self.z),
            (self.x+1, self.y, self.z), (self.x-1, self.y, self.z),
            (self.x, self.y, self.z+1), (self.x, self.y, self.z-1)]

    def coords(self):
        return (self.x, self.y, self.z)


def free_sides(grid, cell: Coord):
    return sum(1 for _ in cell.neighbors() if _ not in grid)


def star1():
    grid = [Coord(*list(map(int, _.split(",")))) for _ in data]
    occupied = [_.coords() for _ in grid]
    return sum(free_sides(occupied, _) for _ in grid)


def bounding_box(grid):
    x = [_[0] for _ in grid]
    y = [_[1] for _ in grid]
    z = [_[2] for _ in grid]
    return ((min(x)-1, min(y)-1, min(z)-1),
            (max(x)+1, max(y)+1, max(z)+1))


def in_boundingbox(n, bb):
    return bb[0][0] <= n[0] <= bb[1][0] and \
           bb[0][1] <= n[1] <= bb[1][1] and \
           bb[0][2] <= n[2] <= bb[1][2]


def flood_fill(start, bb, occupied):
    open_nodes, seen, filled = [start], [], set()
    while open_nodes:
        curr = open_nodes.pop(0)
        for _ in Coord(*curr).neighbors():
            if _ in seen:
                continue
            seen.append(_)
            if _ not in occupied and in_boundingbox(_, bb):
                filled.add(_)
                open_nodes.append(_)

    return filled


def free_sides2(grid, cell: Coord, outside):
    return sum(1 for _ in cell.neighbors()
               if _ not in grid and _ in outside)


def star2():
    grid = [Coord(*list(map(int, _.split(",")))) for _ in data]
    occupied = set([_.coords() for _ in grid])
    bb = bounding_box(occupied)
    outside = flood_fill(bb[0], bb, occupied)

    return sum(free_sides2(occupied, _, outside) for _ in grid)


print("star1:", star1())
print("star2:", star2())
