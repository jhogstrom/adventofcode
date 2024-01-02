from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "23"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_next_cells(s, maze, seen):
    x, y = s
    nextcells = []
    current = maze[s]
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if current == "^" and dy != -1:
            continue
        if current == "v" and dy != 1:
            continue
        if current == "<" and dx != -1:
            continue
        if current == ">" and dx != 1:
            continue
        nextp = (x + dx, y + dy)
        c = maze.get(nextp)
        if c and c in ".<>v^" and nextp not in seen:
            nextcells.append(nextp)
    return nextcells


def print_map(maze, seen):
    maxx = max([x for x, _ in maze.keys()])
    maxy = max([y for _, y in maze.keys()])
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            c = "O" if (x, y) in seen else maze.get((x, y), " ")
            print(c, end="")
        print()
    print("===")


@timeit
def star1(data):
    logging.debug("running star 1")
    maze = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            maze[(x, y)] = data[y][x]

    s = (1, 0)
    seen = {s}
    lengths = []
    junctions = []
    q = deque(seen)
    while q:
        s = q.pop()
        nextcells = get_next_cells(s, maze, seen)
        if len(nextcells) == 0:
            if s == (len(data[0]) - 2, len(data) - 1):
                lengths.append(len(seen)-1)
            if len(junctions) == 0:
                break
            s, seen = junctions.pop()
            q = deque({s})
            continue
        next_cell = nextcells.pop()
        seen.add(next_cell)
        q.append(next_cell)
        for _ in nextcells:
            junctions.append((_, seen.copy()))
    print(max(lengths))



@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
