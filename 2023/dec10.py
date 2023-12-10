from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "10"
year = "2023"
testnum = "4"
if not runtest:
    testnum = ""

set_logging(runtest)
data = get_data(stardate, year, runtest, testnum)
data2 = data[:]


def get_start(data):
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "S":
                return complex(x, y)
    raise ValueError("No start found")


def get_tile(c, data):
    y = int(c.imag)
    x = int(c.real)
    if 0 <= y <= len(data) and 0 <= x <= len(data[y]):
        return data[y][x]
    return "."


NORTH = 0-1j
WEST = -1+0j
SOUTH = 0+1j
EAST = 1+0j

directions = [NORTH, WEST, SOUTH, EAST]


@timeit
def star1(data):
    logging.debug("running star 1")
    start = get_start(data)
    p = start
    comefrom = None
    start_directions = set()
    loop = {}
    while get_tile(p, data) != "S" or not comefrom:
        tile = get_tile(p, data)
        loop[p] = tile
        if tile == "S":
            if get_tile(p + NORTH, data) in "|7F":
                start_directions.add(NORTH)
                comefrom = SOUTH
                p += NORTH
            elif get_tile(p + EAST, data) in "-J7":
                start_directions.add(EAST)
                comefrom = WEST
                p += EAST
            elif get_tile(p + SOUTH, data) in "|LJ":
                start_directions.add(SOUTH)
                comefrom = NORTH
                p += SOUTH
            elif get_tile(p + WEST, data) in "-FL":
                start_directions.add(WEST)
                comefrom = EAST
                p += WEST
        elif tile == "|" and comefrom == SOUTH:
            p += NORTH
            comefrom = SOUTH
        elif tile == "|" and comefrom == NORTH:
            p += SOUTH
            comefrom = NORTH
        elif tile == "7" and comefrom == SOUTH:
            p += WEST
            comefrom = EAST
        elif tile == "7" and comefrom == WEST:
            p += SOUTH
            comefrom = NORTH
        elif tile == "F" and comefrom == SOUTH:
            p += EAST
            comefrom = WEST
        elif tile == "F" and comefrom == EAST:
            p += SOUTH
            comefrom = NORTH
        elif tile == "L" and comefrom == NORTH:
            p += EAST
            comefrom = WEST
        elif tile == "L" and comefrom == EAST:
            p += NORTH
            comefrom = SOUTH
        elif tile == "J" and comefrom == NORTH:
            p += WEST
            comefrom = EAST
        elif tile == "J" and comefrom == WEST:
            p += NORTH
            comefrom = SOUTH
        elif tile == "-" and comefrom == EAST:
            p += WEST
            comefrom = EAST
        elif tile == "-" and comefrom == WEST:
            p += EAST
            comefrom = WEST
        else:
            raise ValueError(f"Unknown tile  {tile} coming from  {comefrom}")
    start_directions.add(comefrom)
    if start_directions == {EAST, WEST}:
        loop[start] = "-"
    elif start_directions == {NORTH, SOUTH}:
        loop[start] = "|"
    elif start_directions == {NORTH, EAST}:
        loop[start] = "L"
    elif start_directions == {NORTH, WEST}:
        loop[start] = "J"
    elif start_directions == {SOUTH, WEST}:
        loop[start] = "7"
    elif start_directions == {SOUTH, EAST}:
        loop[start] = "F"
    else:
        raise ValueError("Unknown direction")
    print("Start1:", len(loop) // 2)

    return loop


charmap = {
    ".": " ",
    " ": ".",
    "L": "└",
    "7": "┐",
    "J": "┘",
    "F": "┌",
    "-": "─",
    "|": "│",
}


@timeit
def star2(data, loop):
    logging.debug("running star 2")
    count = 0
    holes = []
    for y, line in enumerate(data):
        maze = []
        inside = False
        walls = ""
        for x, t in enumerate(line):
            c = complex(x, y)
            tile = loop.get(c, " ")
            if tile in "|":
                walls = tile
            elif tile in "FJ7L":
                walls += tile
            if walls in ["|", "FJ", "L7"]:
                inside = not inside
                walls = ""
            elif walls in ["F7", "LJ"]:
                walls = ""

            if inside and tile == " ":
                count += 1
                holes.append([c, tile])
            p = charmap[tile]
            if p == "." and not inside:
                p = " "
            maze.append(p)
        logging.debug(("".join(maze)))
    # print(holes)
    print("Star2:", count)


loop = star1(data)
star2(data, loop)
