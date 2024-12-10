import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "10"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_starting_points(data):
    starting_points = []
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c == "0":
                starting_points.append((x, y))
    return starting_points


def print_path(data, path):
    for y, s in enumerate(data):
        line = ""
        for x, c in enumerate(s):
            if (x, y) in path:
                line += "X"
            else:
                line += c
        print(line)
    input()


def get_trailheads(data, pos, path) -> int:
    x, y = pos
    value = int(data[y][x])
    if value == 9:
        return [(path[0], pos)]
    result = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = (x + dx, y + dy)
        if 0 <= nx < len(data[0]) and 0 <= ny < len(data):
            next_value = int(data[ny][nx])
            if next_value == value + 1:
                result.extend(get_trailheads(data, (nx, ny), path + [pos]))
    return result


@timeit
def solve(data):
    logging.debug("running star algo")
    starting_points = get_starting_points(data)
    res = []
    for p in starting_points:
        r = get_trailheads(data, p, [p])
        res.extend(r)
    print("star1:", len(set(res)))
    print("star2:", len(res))


solve(data)
