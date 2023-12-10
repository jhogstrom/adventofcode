from collections import defaultdict, deque, namedtuple
import logging
from reader import get_data, timeit, set_logging

runtest = True
stardate = "10"
year = "2023"
testnum = "4"
# testnum = "4"
if not runtest:
    testnum = ""

set_logging(runtest)
data = get_data(stardate, year, runtest, testnum)


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

Target = namedtuple("Target", ["tile", "comefrom"])
Destination = namedtuple("Destination", ["move", "comefrom"])

targets = {
    Target("|", SOUTH): Destination(NORTH, SOUTH),
    Target("|", NORTH): Destination(SOUTH, NORTH),
    Target("7", SOUTH): Destination(WEST, EAST),
    Target("7", WEST): Destination(SOUTH, NORTH),
    Target("F", SOUTH): Destination(EAST, WEST),
    Target("F", EAST): Destination(SOUTH, NORTH),
    Target("L", NORTH): Destination(EAST, WEST),
    Target("L", EAST): Destination(NORTH, SOUTH),
    Target("J", NORTH): Destination(WEST, EAST),
    Target("J", WEST): Destination(NORTH, SOUTH),
    Target("-", EAST): Destination(WEST, EAST),
    Target("-", WEST): Destination(EAST, WEST),
}

map_for_start = {
    (EAST, WEST): "-",
    (WEST, EAST): "-",
    (NORTH, SOUTH): "|",
    (SOUTH, NORTH): "|",
    (NORTH, EAST): "L",
    (EAST, NORTH): "L",
    (NORTH, WEST): "J",
    (WEST, NORTH): "J",
    (SOUTH, WEST): "7",
    (WEST, SOUTH): "7",
    (SOUTH, EAST): "F",
    (EAST, SOUTH): "F",
}


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
        else:
            target = Target(tile, comefrom)
            destination = targets[target]
            p += destination.move
            comefrom = destination.comefrom
    start_directions.add(comefrom)
    loop[start] = map_for_start[tuple(start_directions)]
    print("Start1:", len(loop) // 2)

    return loop


# https://www.sciencebuddies.org/science-fair-projects/references/ascii-table
charmap = {
    " ": " ",
    "L": "└",
    "7": "┐",
    "J": "┘",
    "F": "┌",
    "-": "─",
    "|": "│",
}

BOUNDARIES = ["|", "FJ", "L7"]
BENDS = ["F7", "LJ"]


@timeit
def star2(data, loop):
    logging.debug("running star 2")
    holes = []
    for y, line in enumerate(data):
        maze, inside, walls = [], False, ""
        for x in range(len(line)):
            c = complex(x, y)
            tile = loop.get(c, " ")
            if tile in "|FJ7L":
                walls += tile
            if walls in BOUNDARIES + BENDS:
                if walls in BOUNDARIES:
                    inside = not inside
                walls = ""

            if inside and tile == " ":
                holes.append(c)
                maze.append(".")
            else:
                maze.append(charmap[tile])
        logging.debug(("".join(maze)))
    logging.debug(holes)
    print("Star2:", len(holes))


loop = star1(data)
star2(data, loop)
