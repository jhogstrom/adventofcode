import itertools
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "11"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)


def has_galaxy(data, x, y):
    if "#" in data[y]:
        return True
    return any((_ == "#" for _ in (line[x] for line in data)))


def print_universe(data):
    print("    ", end="")
    for i in range(len(data[0])):
        print(i % 10, end="")
    print()
    for y, line in enumerate(data):
        print(f"{y:3} {line}")
    print("===")


def calculate_distances(data, hubble):
    # Calculate expansion matrix
    matrix = []
    for y in range(len(data)):
        line = []
        for x in range(len(data[y])):
            if has_galaxy(data, x, y):
                line.append(1)
            else:
                line.append(hubble)
        matrix.append(line)
    # # Find galaxies
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "#":
                galaxies.append((x, y))
    res = 0
    # Calculate all distances
    for p in itertools.combinations(galaxies, 2):
        x1 = p[0][0]
        x2 = p[1][0]
        y1 = p[0][1]
        y2 = p[1][1]
        x = matrix[y1][min([x1, x2])+1:max([x1, x2])+1]
        y = [matrix[_][x1] for _ in range(min([y1, y2])+1, max([y1, y2])+1)]
        res += sum(x) + sum(y)

    # print_universe(data)
    # print_universe(matrix)
    return res


@timeit
def star1(data):
    logging.debug("running star 1")
    print(calculate_distances(data, 2))


@timeit
def star2(data):
    logging.debug("running star 2")
    print(calculate_distances(data, 1_000_000))


star1(data)
star2(data)
