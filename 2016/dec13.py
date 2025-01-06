import logging
from collections import deque

from reader import get_data, set_logging, timeit

runtest = False
stardate = "13"
year = "2016"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    magic = int(data[0])
    start = (1, 1)
    target = (7, 4)
    target = (31, 39)
    visited = set()
    q = deque([(start, 0)])
    while q:
        (x, y), steps = q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == target:
            print(steps)
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            newx, newy = x + dx, y + dy
            if newx < 0 or newy < 0:
                continue
            if (
                bin(
                    (newx * newx + 3 * newx + 2 * newx * newy + newy + newy * newy)
                    + magic
                ).count("1")
                % 2
            ):
                continue
            q.append(((newx, newy), steps + 1))


@timeit
def star2(data):
    logging.debug("running star 2")
    magic = int(data[0])
    start = (1, 1)
    visited = set()
    q = deque([(start, 0)])
    while q:
        (x, y), steps = q.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if steps >= 50:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            newx, newy = x + dx, y + dy
            if newx < 0 or newy < 0:
                continue
            if (
                bin(
                    (newx * newx + 3 * newx + 2 * newx * newy + newy + newy * newy)
                    + magic
                ).count("1")
                % 2
            ):
                continue
            q.append(((newx, newy), steps + 1))
    print(len(visited))


star1(data)
star2(data2)
