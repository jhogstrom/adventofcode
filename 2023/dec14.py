import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "14"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)

moves = {
    "south": lambda p: (p[0], p[1]+1),
    "west": lambda p: (p[0]-1, p[1]),
    "east": lambda p: (p[0]+1, p[1]),
    "north": lambda p: (p[0], p[1]-1),
}


def move_cell(p, matrix, direction):
    # logging.debug(f"Moving cell {x}, {y}")
    if matrix[p] != "O":
        return
    while matrix.get(moves[direction](p), "#") == ".":
        matrix[p] = "."
        p = moves[direction](p)
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
    tilt("north", matrix, data)
    print(board_load(matrix, data))


def cycle_board(matrix, data):
    tilt("north", matrix, data)
    tilt("west", matrix, data)
    tilt("south", matrix, data)
    tilt("east", matrix, data)


@timeit
def star2(data):
    logging.debug("running star 2")
    matrix = define_matrix(data)
    all_grids = []

    while True:
        cycle_board(matrix, data)
        if matrix in all_grids:
            break
        all_grids.append(matrix.copy())

    MAXITER = 1_000_000_000
    period = len(all_grids) - all_grids.index(matrix)
    loop_start = all_grids.index(matrix)

    index = (MAXITER - loop_start) % period + loop_start - 1
    # print(f"Loop start: {loop_start}. Period:  {period}. Index {index}")
    print(board_load(all_grids[index], data))


star1(data)
star2(data)
