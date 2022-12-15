import os

runtest = False
stardate = "15"
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Coord():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def dist(self, c):
        return abs(self.x - c.x) + abs(self.y - c.y)

    def coord(self):
        return (self.x, self.y)


def get_coord(s):
    p = s.split()
    x = int(p[-2][2:-1])
    y = int(p[-1][2:])
    return Coord(x, y)


def parse(data):
    grid = {}
    for _ in data:
        p = _.split(":")
        s = get_coord(p[0])
        b = get_coord(p[1])
        grid[s] = b
    return grid


def star1():
    target = 2000000 if not runtest else 10
    grid = parse(data)

    blocked = set()
    beacons = set()

    for s, b in grid.items():
        d = s.dist(b)
        if b.y == target:
            beacons.add(b.coord())
        if s.y - d < target < s.y + d:
            for x in range(s.x-(d - abs(s.y-target)), s.x+(d - abs(s.y-target)) + 1):
                blocked.add((x, target))

    return len(blocked) - len(beacons)


def get_ranges(target, grid):
    ranges = []

    for s, b in grid.items():
        d = s.dist(b)
        if s.y - d < target < s.y + d:
            ranges.append((s.x-(d - abs(s.y-target)), s.x+(d - abs(s.y-target)) + 1))

    ranges = sorted(ranges)

    r = 0
    while r < len(ranges)-1:
        if ranges[r][1] > ranges[r+1][0]:
            ranges[r+1] = (ranges[r][0], max([ranges[r][1], ranges[r+1][1]]))
            ranges.pop(r)
        else:
            r += 1
    return ranges


def star1_2():
    """
    Reimplemented *1 using the marged range-koncept
    learned in *2.
    It has some shortcomings, though, as there may very well be
    more than 1 range, a situation that would yield a lower answer.
    """
    grid = parse(data)
    target = 10 if runtest else 2_000_000
    ranges = get_ranges(target, grid)
    b = set()
    for _ in grid.values():
        if _.y == target:
            b.add((_.x, _.y))
    return ranges[0][1]-ranges[0][0]-len(b)


def star2():
    grid = parse(data)
    maxrow = 20 if runtest else 4_000_000
    for r in range(maxrow):
        ranges = get_ranges(r, grid)
        if len(ranges) > 1:
            break
    return r + ranges[0][1] * 4_000_000


print("star1:", star1())
print("faster star1:", star1_2())
print("star2:", star2())
