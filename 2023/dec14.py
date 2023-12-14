from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "14"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def next_cell(p, direction):
    if direction == "south":
        return (p[0], p[1]+1)
    if direction == "west":
        return (p[0]-1, p[1])
    if direction == "east":
        return (p[0]+1, p[1])
    if direction == "north":
        return (p[0], p[1]-1)
    raise ValueError(f"Unknown direction {direction}")


def move_cell(p, matrix, direction):
    # logging.debug(f"Moving cell {x}, {y}")
    if matrix[p] != "O":
        return
    while matrix.get(next_cell(p, direction), "#") == ".":
        matrix[p] = "."
        p = next_cell(p, direction)
        matrix[p] = "O"


def print_board(matrix, data):
    for y in range(len(data)):
        for x in range(len(data[0])):
            print(matrix[(x, y)], end="")
        print()
    print("===")


def board_load(matrix, data):
    res = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if matrix[(x, y)] == "O":
                res += len(data) - y
    return res


def define_matrix(data):
    res = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            res[(x, y)] = data[y][x]
    return res


def tilt(direction, matrix, data):
    # logging.debug(f"Tilting {direction}")
    if direction == "north":
        for y in range(len(data)):
            for x in range(len(data[0])):
                move_cell((x, y), matrix, direction)
    elif direction == "south":
        for y in range(len(data)-1, -1, -1):
            for x in range(len(data[0])):
                move_cell((x, y), matrix, direction)
    elif direction == "west":
        for x in range(len(data[0])):
            for y in range(len(data)):
                move_cell((x, y), matrix, direction)
    elif direction == "east":
        for x in range(len(data[0])-1, -1, -1):
            for y in range(len(data)):
                move_cell((x, y), matrix, direction)
    else:
        raise ValueError(f"Unknown direction {direction}")
    return matrix


@timeit
def star1(data):
    logging.debug("running star 1")
    matrix = define_matrix(data)
    matrix = tilt("north", matrix, data)
    print(board_load(matrix, data))


def cycle_board(matrix, data):
    matrix = tilt("north", matrix, data)
    matrix = tilt("west", matrix, data)
    matrix = tilt("south", matrix, data)
    matrix = tilt("east", matrix, data)
    return matrix


def detect_loop(thelist):
    looplen = 2
    fast = 1
    slow = 0
    mu = 0
    loop1 = False
    lam = 0
    while fast+looplen < len(thelist) and slow < len(thelist):
        fast += looplen
        slow += 1
        mu += 1
        lam += 1
        if thelist[fast] == thelist[slow] and lam > 1:
            if loop1:
                # print(f"Start pos: {mu-lam} - len = {lam}")
                return (True, mu-lam, lam)
            else:
                lam = 0
            loop1 = True
    return (False, 0, 0)


@timeit
def star2(data):
    logging.debug("running star 2")
    matrix = define_matrix(data)
    c = 0
    loads = []

    while not detect_loop(loads)[0]:
        cycle_board(matrix, data)
        c += 1
        loads.append(board_load(matrix, data))
        # print_board(matrix, data)
        print(c, loads[-1])

    MAXITER = 1_000_000_000
    _, loop_start, period = detect_loop(loads)
    print(f"Loop start: {loop_start}. Period:  {period}")
    index1 = (MAXITER - loop_start) % period
    index2 = MAXITER - (MAXITER//period)*period

    print(index1, index2)
    print("index1: ", loads[loop_start + index1])
    print("index2 ", loads[loop_start + index2])
    print("104639 is too high")


star1(data)
star2(data2)
