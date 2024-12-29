import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "18"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def parse_data(data):
    result = set()
    for line in data:
        p = tuple(int(_) for _ in line.split(","))
        result.add(p)
    return result


def get_neighbors(pos, grid, bounds):
    result = []
    for p in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x = pos[0] + p[0]
        y = pos[1] + p[1]
        if (
            (x, y) not in grid
            and x >= 0
            and y >= 0
            and x <= bounds[0]
            and y <= bounds[1]
        ):
            result.append((x, y))
    return result


def print_grid(grid, bounds, seen=None):
    for y in range(bounds[1] + 1):
        for x in range(bounds[0] + 1):
            if (x, y) in grid:
                print("#", end="")
            elif seen and (x, y) in seen:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print("===")


def floodfill(grid, bounds, pos):
    edge = [(pos, 0)]
    seen = {pos: 0}
    while edge:
        pos, cost = edge.pop(0)
        for p in get_neighbors(pos, grid, bounds):
            if p in seen:
                continue
            seen[p] = min(seen.get(p, cost + 1), cost + 1)
            edge.append((p, cost + 1))

    return seen.get(bounds)


@timeit
def star1(data):
    logging.debug("running star 1")
    pos = (0, 0)
    if runtest:
        lines = 12
        bounds = (6, 6)
    else:
        lines = 1024
        bounds = (70, 70)
    grid = parse_data(data[:lines])
    print(floodfill(grid, bounds, pos))


@timeit
def star2(data):
    logging.debug("running star 2")
    pos = (0, 0)
    if runtest:
        lines = 12
        bounds = (6, 6)
    else:
        lines = 1024
        bounds = (70, 70)
    while True:
        grid = parse_data(data[:lines])
        res = floodfill(grid, bounds, pos)
        if res is None:
            break
        # print(f"{lines} - {data[lines-1]} worked")
        lines += 1
    print(data[lines - 1])


star1(data)
star2(data2)
