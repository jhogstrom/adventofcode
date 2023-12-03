import logging
from math import prod
from reader import get_data, timeit, set_logging

runtest = False
stardate = "3"

set_logging(runtest)
data = get_data(stardate, runtest)

data2 = data[:]


def get_neighbors(c):
    return [
        (c[0]-1, c[1]-1), (c[0], c[1]-1), (c[0]+1, c[1]-1),
        (c[0]-1, c[1]),                   (c[0]+1, c[1]),
        (c[0]-1, c[1]+1), (c[0], c[1]+1), (c[0]+1, c[1]+1),
        ]


def parse_data(data):
    schema = {}
    nummap = []
    for y, line in enumerate(data):
        number = ""
        coordinates_for_number = []
        for x, c in enumerate(line):
            schema[(x, y)] = c
            if c.isdigit():
                number += c
                coordinates_for_number.append((x, y))
            else:
                if number:
                    nummap.append([int(number), coordinates_for_number])
                    number = ""
                    coordinates_for_number = []
        if number:
            nummap.append([int(number), coordinates_for_number])
    return schema, nummap


@timeit
def star1(data):
    schema, nummap = parse_data(data)

    res = 0
    for numdata in nummap:
        n, coords = numdata
        neighbor_set = set()
        for c in coords:
            neighbors = get_neighbors(c)
            for _ in neighbors:
                neighbor_set.add(_)

        next_to_symbol = False
        for _ in neighbor_set:
            nc = schema.get(_, ".")
            if nc != "." and not nc.isdigit():
                next_to_symbol = True
                break
        if next_to_symbol:
            res += n
    print(res)


@timeit
def star2(data):
    schema, nummap = parse_data(data)
    res = 0

    for c, v in schema.items():
        if v != "*":
            continue
        neighbors = get_neighbors(c)
        gearparts = []
        for n in neighbors:
            for _ in nummap:
                if n in _[1] and _ not in gearparts:
                    gearparts.append(_)
        if len(gearparts) == 2:
            res += prod([_[0] for _ in gearparts])

    print(res)


star1(data)
star2(data2)
