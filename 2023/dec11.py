import itertools
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "11"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)


def empty_row(data, y):
    return "#" not in data[y]


def empty_col(data, x):
    for line in data:
        if line[x] == "#":
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


def calculate_distances(data, hubble):
    # Calculate expansion matrix
    matrix = []
    for y in range(len(data)):
        line = []
        for x in range(len(data[y])):
            if empty_col(data, x) or empty_row(data, y):
                line.append(hubble)
            else:
                line.append(1)
        matrix.append(line)
    # Find galaxies
    galaxies = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "#":
                galaxies.append((x, y))
    # print_universe(data)
    res = 0
    # Calculate all distances
    for p in itertools.combinations(galaxies, 2):
        x = matrix[p[0][1]][min([p[0][0], p[1][0]])+1:max([p[0][0], p[1][0]])+1]
        y = [matrix[_][p[0][0]] for _ in range(min([p[0][1], p[1][1]])+1, max([p[0][1], p[1][1]])+1)]
        res += sum(x) + sum(y)

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
