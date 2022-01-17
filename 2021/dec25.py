import os
from timer import timeit
from collections import defaultdict, deque

stardate = 25
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
# dataname = f"dec{stardate}_ex1.txt"
# dataname = f"dec{stardate}_ex2.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


RIGHT = ">"
DOWN = "v"

def get_next_c_down(board, c, xmax, ymax):
    resy = c[1]+1 if c[1] < ymax-1 else 0
    new_c = (c[0], resy)
    if not board[new_c]:
        # print(f"{breed} @ {(x, y)} moves to {(x, resy)}")
        return new_c, True
    return c, False


def get_next_c_right(board, c, xmax, ymax):
    resx = c[0]+1 if c[0] < xmax-1 else 0
    new_c = (resx, c[1])
    if not board[new_c]:
        # print(f"{breed} @ {(x, y)} moves to {(resx, y)}")
        return new_c, True
    return c, False


get_next_c = {
    DOWN: get_next_c_down,
    RIGHT: get_next_c_right
}


def move_cucumbers(board, breed, *, xmax, ymax):
    hasmoved = False
    nextgen = []

    for x in range(xmax):
        for y in range(ymax):
            c = (x, y)
            if board[c] == breed:
                next_c, didMove = get_next_c[breed](board, c, xmax, ymax)
                hasmoved |= didMove
                nextgen.append(next_c)
    return hasmoved, nextgen


def print_out(gencount, board, xmax, ymax):
    print(f"After {gencount} steps")
    for y in range(ymax):
        for x in range(xmax):
            print(board[(x, y)], end="")
        print()
    print("===")


def update_board(board: dict, nextgen: list, breed):
    res = defaultdict(bool)
    for _, v in board.items():
        if v != breed:
            res[_] = v
    for _ in nextgen:
        res[_] = breed
    return res


@timeit
def star1(data):
    board = defaultdict(bool)
    for y in range(len(data)):
        for x in range(len(data[y])):
            board[(x, y)] = False if data[y][x] == '.' else data[y][x]
    xmax, ymax, moved_right, moved_down, gencount = x+1, y+1, True, True, 0
    # print_out(gencount, board, xmax, ymax)
    while moved_right or moved_down:
        gencount += 1
        moved_right, nextgen = move_cucumbers(board, RIGHT, xmax=xmax, ymax=ymax)
        board = update_board(board, nextgen, RIGHT)

        moved_down, nextgen = move_cucumbers(board, DOWN, xmax=xmax, ymax=ymax)
        board = update_board(board, nextgen, DOWN)

        # print_out(gencount, board, xmax, ymax)
    print(gencount)


star1(data)
