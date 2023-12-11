from collections import defaultdict, deque
import itertools
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "11"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def isempty(data, x):
    for y in range(len(data)):
        if data[y][x] == "#":
            return False
    return True


def print_universe(data):
    print("    ", end="")
    for i in range(len(data[0])):
        print(i%10, end="")
    print()
    for y, line in enumerate(data):
        print(f"{y:3} {line}")
    print("===")

@timeit
def star1(data):
    logging.debug("running star 1")
    # print_universe(data)
    # Expand universe
    expanded = []
    for line in data:
        expanded.append(line)
        if "#" not in line:
            expanded.append(line)
    data = expanded[:]
    expanded = ["" for _ in data]
    for x in range(len(data[0])):
        empty = isempty(data, x)
        for _ in range(len(expanded)):
            expanded[_] += data[_][x]
            if empty:
                expanded[_] += "."
    data = expanded[:]
    # print_universe(data)
    # Find galaxies
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "#":
                galaxies.append((x, y))
    # print(galaxies)
    # Find pairs
    res = 0
    for p in itertools.combinations(galaxies, 2):
        d = abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1])
        res += d

    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    # print_universe(data)
    # Expand universe
    expanded = []
    for line in data:
        expanded.append(line)
        if "#" not in line:
            expanded.append("x"*len(line))
    data = expanded[:]
    expanded = ["" for _ in data]
    for x in range(len(data[0])):
        empty = isempty(data, x)
        for _ in range(len(expanded)):
            expanded[_] += data[_][x]
            if empty:
                expanded[_] += "x"
    data = expanded[:]
    # print_universe(data)
    # Find galaxies
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "#":
                galaxies.append((x, y))
    # print(galaxies)
    # Find pairs
    res = 0
    hubble = 1000_000
    for p in itertools.combinations(galaxies, 2):
        x_string = data[p[0][1]][min([p[0][0], p[1][0]])+1:max([p[0][0],p[1][0]])+1]
        y_string = "".join([data[_][p[0][0]] for _ in range(min([p[0][1], p[1][1]])+1, max([p[0][1], p[1][1]])+1)])
        xdist = sum([1 if _ in "#." else hubble-1 for _ in x_string])
        ydist = sum([1 if _ in "#." else hubble-1 for _ in y_string])
        d = xdist + ydist
        res += d

    print(res)



star1(data)
star2(data2)
