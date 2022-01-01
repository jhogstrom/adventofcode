import os
import inspect
from typing import Dict, Tuple
from timer import timeit
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO, format="")
logger = logging.getLogger()

stardate = 22
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test2.txt"
# dataname = f"dec{stardate}_ex1.txt"
# dataname = f"dec{stardate}_ex2.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")

def parse_instruction(s):
    def parse_coords(s):
        _, coords = s.split("=")
        coords = [int(_) for _ in coords.split("..")]
        return [min(coords), max(coords)]

    command, values = s.split()
    command = command == "on"
    coords = []

    for d in range(3):
        coords.append(parse_coords(values.split(",")[d]))
    logger.debug(s)
    return command, coords


class CoordinateHolder():
    def __init__(self, command, coords) -> None:
        self.command = command
        self.coords = coords

    def __str__(self) -> str:
        switchmap = {True: "on", False: "off"}
        dims = "xyz"
        ranges = []
        for d in range(3):
            ranges.append(f"{dims[d]}={self.coords[d][0]}..{self.coords[d][1]}")
        return f"{switchmap[self.command]} {','.join(ranges)}"


class Instruction(CoordinateHolder):
    def n_range(self, d):
        _from = max([self.coords[d][0], -50])
        _to = min([self.coords[d][1], 50]) + 1
        return range(_from, _to)

    def xrange(self):
        return self.n_range(0)

    def yrange(self):
        return self.n_range(1)

    def zrange(self):
        return self.n_range(2)

    def toggle(self, cube: Dict[Tuple, bool]):
        for x in self.xrange():
            for y in self.yrange():
                for z in self.zrange():
                    cube[(x, y, z)] = self.command


class Coord():
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Cuboid(CoordinateHolder):
    def __init__(self, command, coords) -> None:
        super().__init__(command, coords)
        self.corners = [
            Coord(self.x[0], self.y[0], self.z[0]),  # TLF
            Coord(self.x[1], self.y[0], self.z[0]),  # TRF
            Coord(self.x[0], self.y[1], self.z[0]),  # BLF
            Coord(self.x[1], self.y[1], self.z[0]),  # BRF
            Coord(self.x[0], self.y[0], self.z[1]),  # TLB
            Coord(self.x[1], self.y[0], self.z[1]),  # TRB
            Coord(self.x[0], self.y[1], self.z[1]),  # BLB
            Coord(self.x[1], self.y[1], self.z[1]),  # BRB
        ]

    def __str__(self) -> str:
        return f"{super().__str__()} - Size: {self.volume}"

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    @property
    def width(self):
        return self.x[1] - self.x[0] + 1

    @property
    def height(self):
        return self.y[1] - self.y[0] + 1

    @property
    def depth(self):
        return self.z[1] - self.z[0] + 1

    @property
    def volume(self):
        return self.width * self.height * self.depth

    def contains(self, coord: Coord):
        return self.x[0] <= coord.x <= self.x[1] \
            and self.y[0] <= coord.y <= self.y[1] \
            and self.z[0] <= coord.z <= self.z[1]

    def overlaps(self, cuboid):
        if any(self.contains(_) for _ in cuboid.corners):
            return True
        if cuboid.x[1] < self.x[0] or cuboid.x[0] > self.x[1]:  # Left or right of
            return False
        if cuboid.y[1] < self.y[0] or cuboid.y[0] > self.y[1]:  # above or under
            return False
        if cuboid.z[1] < self.z[0] or cuboid.z[0] > self.z[1]:  # in front of or behind
            return False
        return True

    def split_x_left(self, x):
        res = Cuboid(self.command, [[self.x[0], x-1], self.y[:], self.z[:]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.x[0] = x
        return res

    def split_x_right(self, x):
        res = Cuboid(self.command, [[x+1, self.x[1]], self.y[:], self.z[:]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.x[1] = x
        return res

    def split_y_top(self, y):
        res = Cuboid(self.command, [self.x[:], [self.y[0], y-1], self.z[:]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.y[0] = y
        return res

    def split_y_bottom(self, y):
        res = Cuboid(self.command, [self.x[:], [y+1, self.y[1]], self.z[:]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.y[1] = y
        return res

    def split_z_front(self, z):
        res = Cuboid(self.command, [self.x[:], self.y[:], [self.z[0], z-1]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.z[0] = z
        return res

    def split_z_behind(self, z):
        res = Cuboid(self.command, [self.x[:], self.y[:], [z+1, self.z[1]]])
        logger.debug(f"{inspect.currentframe().f_code.co_name}: {res}")
        self.z[1] = z
        return res

    def merge(self, cuboid):
        # Split the incoming cuboid, returning a list of smaller segments that
        # does not include self.
        # Case 0: The two cuboids are completely disjoint, no new splits are created.
        if not self.overlaps(cuboid):
            return [cuboid]

        # case 1: self fully encloses cuboid. Only self remains.
        # +-----------+ <= self
        # | +-----+   |
        # | |     |   |
        # | +-----+   |
        # +-----------+
        #
        if self.x[0] < cuboid.x[0] and self.x[1] > cuboid.x[1] \
            and self.y[0] < cuboid.y[0] and self.y[1] > cuboid.y[1] \
            and self.z[0] < cuboid.z[0] and self.z[1] > cuboid.z[1]:
            return []

        # There is overlap (including full containment), so start splitting the cuboid in each dimension,
        # leaving self intact.
        # The result should be a set of cuboids that make up the intersection of the cuboid and self,
        # with self still in one piece.
        # case 2-x
        # +-----...               +---+-...
        # |   +-...   <= self     |   +-...
        # |   |                => |   |
        # |   +-...               |   +-...
        # +-----...               +---+-...

        res = []
        if cuboid.x[0] < self.x[0]:
            res.append(cuboid.split_x_left(self.x[0]))
        if cuboid.x[1] > self.x[1]:
            res.append(cuboid.split_x_right(self.x[1]))
        if cuboid.y[0] < self.y[0]:
            res.append(cuboid.split_y_top(self.y[0]))
        if cuboid.y[1] > self.y[1]:
            res.append(cuboid.split_y_bottom(self.y[1]))
        if cuboid.z[0] < self.z[0]:
            res.append(cuboid.split_z_front(self.z[0]))
        if cuboid.z[1] > self.z[1]:
            res.append(cuboid.split_z_behind(self.z[1]))
        return res


@timeit
def star1(data):
    instructions = [Instruction(*parse_instruction(_)) for _ in data]
    cube = defaultdict(bool)
    for i in instructions:
        i.toggle(cube)

    print(list(cube.values()).count(True))


@timeit
def star2(data):
    cubes = [Cuboid(*parse_instruction(_)) for _ in data[:]]
    print("Cubes/instructions", len(cubes))
    cuboids = []

    for cube in cubes:
        logger.debug(f"Instruction: {cube}")
        new_cuboids = []
        for cuboid in cuboids:
            new_cuboids.extend(cube.merge(cuboid))
        new_cuboids.append(cube)
        cuboids = new_cuboids[:]
        logger.debug("Split cuboids", len(cuboids))
    for _ in cuboids:
        logger.debug(f"{_}")
    count = sum(_.volume for _ in cuboids if _.command)
    print("Total count", count)
    # print("Expected...", 2758514936282235)


# star1(data)
star2(data)
