import logging
from collections import defaultdict
from typing import List, Tuple  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "14"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


class Robot:
    def __init__(self, start: Tuple[int, int], v: Tuple[int, int]):
        self._pos = start
        self.v = v

    def __str__(self):
        return f"p={(self._pos)}, v={self.v}"

    def move(self, steps: int):
        self._pos = (
            (self._pos[0] + self.v[0] * steps),
            (self._pos[1] + self.v[1] * steps),
        )

    def pos(self, bounds: Tuple[int, int]):
        return ((self._pos[0] % bounds[0]), (self._pos[1] % bounds[1]))

    def sector(self, bounds: Tuple[int, int]) -> Tuple[int, int]:
        mid_x = bounds[0] // 2
        mid_y = bounds[1] // 2
        pos = self.pos(bounds)
        if pos[0] < mid_x and pos[1] < mid_y:
            return 1
        if pos[0] > mid_x and pos[1] < mid_y:
            return 2
        if pos[0] < mid_x and pos[1] > mid_y:
            return 3
        if pos[0] > mid_x and pos[1] > mid_y:
            return 4
        return 0


def parse_robots(data) -> List[Robot]:
    result = []
    for line in data:
        p, v = line.split()
        p = tuple(int(_) for _ in p.split("=")[1].split(","))
        v = tuple(int(_) for _ in v.split("=")[1].split(","))
        result.append(Robot(p, v))
    return result


def print_robots(robots):
    for r in robots:
        print(r)


def calc_field(robots, bounds):
    positions = [r.pos(bounds) for r in robots]
    result = []
    for y in range(bounds[1]):
        line = []
        for x in range(bounds[0]):
            if (x, y) in positions:
                line.append(positions.count((x, y)))
            else:
                line.append(0)
        result.append(line)
    return result


def print_field(robots, bounds, wait: bool = False):
    # center_lines = set((mid_x, y) for y in range(bounds[1])) | set((x, mid_y) for x in range(bounds[0]))

    result = calc_field(robots, bounds)

    for y, line in enumerate(result):
        for x, c in enumerate(line):
            # if (x, y) in center_lines:
            #     print(" ", end="")
            # else:
            print(c if c else " ", end="")
        print("<")
    print()
    if wait:
        input()


@timeit
def star1(data):
    logging.debug("running star 1")
    robots = parse_robots(data)

    if runtest:
        bounds = (11, 7)
    else:
        bounds = (101, 103)
    [r.move(100) for r in robots]
    # print_field(robots, bounds)

    sectors = defaultdict(int)
    for r in robots:
        sectors[r.sector(bounds)] += 1
    del sectors[0]

    security = 1
    for i in sorted(sectors):
        security *= sectors[i]

    print(security)


def line_full(robots, bounds) -> bool:
    SCANLINE = 50
    positions = set(r.pos(bounds) for r in robots)
    positions = set(_[0] for _ in positions if _[1] == SCANLINE)
    line = []
    for x in range(bounds[0]):
        line.append("X" if x in positions else " ")
    return "XXXXXX" in "".join(line)


@timeit
def star2(data):
    logging.debug("running star 2")
    robots = parse_robots(data)

    if runtest:
        bounds = (11, 7)
    else:
        bounds = (101, 103)

    seconds = 0

    while seconds < 1000_000:
        seconds += 1
        [r.move(1) for r in robots]
        if line_full(robots, bounds):
            print(f"Seconds: {seconds}")
            print_field(robots, bounds, False)
            print("====================================")
            break
    print(seconds)


star1(data)
star2(data2)
