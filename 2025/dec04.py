import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "04"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_neighbors_count(x, y, data):
    max_y = len(data)
    max_x = len(data[0])
    directions = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    count = 0
    for direction in directions:
        dx, dy = direction
        if x + dx < 0 or y + dy < 0:
            return 0
        if x + dx >= max_x or y + dy >= max_y:
            return 0
        if data[y + dy][x + dx] == "@":
            count += 1
    return count


@timeit
def star1(data):
    logging.debug("running star 1")
    data = [list(line) for line in data]
    res = 0
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            n = get_neighbors_count(x, y, data)
            if c == "@" and n < 4:
                res += 1
    logging.info(f"star 1: {res}")


@timeit
def star2(data):
    logging.debug("running star 2")
    data = [list(line) for line in data]
    res = 1
    removed = 0
    while res > 0:
        removable = []
        res = 0
        for y, line in enumerate(data):
            for x, c in enumerate(line):
                n = get_neighbors_count(x, y, data)
                if c == "@" and n < 4:
                    res += 1
                    removed += 1
                    removable.append((x, y))
        for x, y in removable:
            data[y][x] = "."
    logging.info(f"star 2: {removed}")


star1(data)
star2(data2)
