import logging
from collections import defaultdict
from itertools import combinations

from reader import get_data, set_logging, timeit

runtest = False
stardate = "08"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def in_bounds(p, bounds):
    x, y = p
    x1, y1 = bounds[0]
    x2, y2 = bounds[1]
    return x1 <= x < x2 and y1 <= y < y2


def create_node(a1, a2, bounds):
    x1, y1 = a1
    x2, y2 = a2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    nodes = []
    if x1 == x2:
        nodes.append((x1 - dx, min(y1, y2) - dy))
        nodes.append((x1 + dx, max(y1, y2) + dy))
    elif y1 == y2:
        nodes.append((min(x1, x2) - dx, y1 - dy))
        nodes.append((max(x1, x2) + dx, y1 + dy))
    elif x1 < x2 and y1 < y2:
        nodes.append((x1 - dx, y1 - dy))
        nodes.append((x2 + dx, y2 + dy))
    elif x1 < x2 and y1 > y2:
        nodes.append((x1 - dx, y1 + dy))
        nodes.append((x2 + dx, y2 - dy))
    elif x1 > x2 and y1 < y2:
        nodes.append((x1 + dx, y1 - dy))
        nodes.append((x2 - dx, y2 + dy))
    elif x1 > x2 and y1 > y2:
        nodes.append((x1 + dx, y1 + dy))
        nodes.append((x2 - dx, y2 - dy))
    return [(in_bounds(node, bounds), node) for node in nodes]


def print_map(freq, antennas, data, nodes):
    print(f"Antenna '{freq}' at {antennas} -> {nodes}")
    for y, s in enumerate(data):
        line = ""
        for x, c in enumerate(s):
            if (x, y) in nodes:
                line += "#"
            # elif (x, y) in antennas:
            #     line += "X"
            else:
                line += c
        print(line)
    input()


def add(p, d) -> tuple[int, int]:
    return (p[0] + d[0], p[1] + d[1])


def traverse(start, d, bounds):
    result = set()
    p = start
    while in_bounds(add(p, d), bounds):
        p = add(p, d)
        result.add(p)
    p = start
    di = (-d[0], -d[1])
    while in_bounds(add(p, di), bounds):
        p = add(p, di)
        result.add(p)
    return result


def create_multi_node(a1, a2, bounds):
    x1, y1 = a1
    x2, y2 = a2
    dx = x2 - x1
    dy = y2 - y1
    return {a1, a2}.union(traverse(a1, (dx, dy), bounds))


def get_beacons(data):
    beacons = defaultdict(list)
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c != ".":
                beacons[c].append((x, y))
    return beacons


@timeit
def star1(data):
    logging.debug("running star 1")
    beacons = get_beacons(data)
    bounds = ((0, 0), (len(data[0]), len(data)))
    result = set()

    for k, v in beacons.items():
        for p in combinations(v, 2):
            result.update(node for ok, node in create_node(p[0], p[1], bounds) if ok)

    print(len(result))


@timeit
def star2(data):
    logging.debug("running star 2")
    beacons = get_beacons(data)
    bounds = ((0, 0), (len(data[0]), len(data)))
    result = set()

    for _, v in beacons.items():
        for p in combinations(v, 2):
            result.update(create_multi_node(p[0], p[1], bounds))

    print(len(result))


star1(data)
star2(data2)
