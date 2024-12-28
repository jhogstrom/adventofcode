import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "16"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_pos(data, target):
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == target:
                return (x, y)


directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def add_pos(pos, d):
    return (pos[0] + d[0], pos[1] + d[1])


def get_neighbors(pos, data):
    res = []
    for p in directions.values():
        next = add_pos(pos, p)
        if data[next[1]][next[0]] != "#":
            res.append(next)
    return res


def new_direction(from_pos, to_pos):
    for d, v in directions.items():
        if add_pos(from_pos, v) == to_pos:
            return d
    raise ValueError(f"Lost all sense of direction going from {from_pos} to {to_pos}")


def print_maze(pos, data, seen):
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if (x, y) == pos:
                print("X", end="")
            elif (x, y) in seen:
                print("o", end="")
            else:
                print(c, end="")
        print()


def traverse_map(data):
    pos = get_pos(data, "S")
    endpos = get_pos(data, "E")
    d = "E"

    seen = {pos}
    crossroads = []
    costs = []
    cost = 0
    while True:
        next_steps = [_ for _ in get_neighbors(pos, data) if _ not in seen]
        seen.add(pos)
        # At a fork in the road? Save the cost and new direction if moving to all but one
        while len(next_steps) > 1:
            fork = next_steps.pop()
            fork_dir = new_direction(pos, fork)
            next_cost = cost + (1 if fork_dir == d else 1001)
            crossroads.append((fork, next_cost, fork_dir, seen.copy()))
        # At a dead end? Go back to the last fork in the road
        if not next_steps:
            if not crossroads:
                break
            pos, cost, d, seen = crossroads.pop()
            continue
        # Move to the next step, which is turning or straight ahead
        new_dir = new_direction(pos, next_steps[0])
        cost += 1 if new_dir == d else 1001
        pos = next_steps[0]
        d = new_dir
        # Arrived at the end? Print the cost and go back to the last fork in the road
        if pos == endpos:
            costs.append(cost)
            # print(cost)
            pos, cost, d, seen = crossroads.pop()
        # print_maze(pos, data, seen)
        # print(crossroads)
        # input()
    return min(costs)


def floodfill(data):
    pos = get_pos(data, "S")
    endpos = get_pos(data, "E")

    visited = {pos: (0, "E")}
    edges = [pos]
    costs = []

    while edges:
        pos = edges.pop()
        cost, direction = visited[pos]
        next_pos = get_neighbors(pos, data)
        for n in next_pos:
            next_dir = new_direction(pos, n)
            next_cost = cost + (1 if next_dir == direction else 1001)
            if n == endpos:
                costs.append(next_cost)
            elif n not in visited or next_cost < visited[n][0]:
                visited[n] = (next_cost, next_dir)
                edges.append(n)
    return min(costs)


@timeit
def star1(data):
    logging.debug("running star 1")
    # print(traverse_map(data))
    print(floodfill(data))


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
