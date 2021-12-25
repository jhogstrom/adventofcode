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

def constant_factory(value):
    return lambda: value

# class Board():
#     def __init__(self, data) -> None:
#         pass

moved = False

def get_next_c(board, x, y, breed, xmax, ymax):
    global moved
    if breed == ">":
        resx = x+1 if x < xmax-1 else 0
        if board[(resx, y)] == ".":
            # print(f"{breed} @ {(x, y)} moves to {(resx, y)}")
            moved = True
            return (resx, y)
        return (x, y)
    if breed == "v":
        resy = y+1 if y < ymax-1 else 0
        if board[(x, resy)] == ".":
            # print(f"{breed} @ {(x, y)} moves to {(x, resy)}")
            moved = True
            return (x, resy)
        return x, y
    raise

def move_cucumbers(board, breed, *, xmax, ymax, nextgen):
    # hasmoved = False
    for x in range(xmax):
        for y in range(ymax):
            if board[(x, y)] == breed:
                next_c = get_next_c(board, x, y, breed, xmax, ymax)
                nextgen[next_c] = breed
                # hasmoved |= next_c == (x, y)
    # return hasmoved

def print_out(gencount, board, xmax, ymax):
    print(f"After {gencount} steps")
    for y in range(ymax):
        for x in range(xmax):
            print(board[(x, y)], end="")
        print()
    print("===")

def update_board(board, nextgen, breed):
    moved = [_ for _ in board if board[_] == breed]
    for _ in moved:
        board.pop(_)
    for _ in nextgen:
        board[_] = nextgen[_]


@timeit
def star1(data):
    global moved
    board = defaultdict(constant_factory('.'))
    for y in range(len(data)):
        for x in range(len(data[y])):
            board[(x, y)] = data[y][x]
    xmax, ymax = x+1, y+1
    moved = True
    gencount = 0
    # print_out(gencount, board, xmax, ymax)
    while moved:
        moved = False
        gencount += 1
        nextgen = defaultdict(constant_factory('.'))
        move_cucumbers(board, ">",
            xmax=xmax, ymax=ymax, nextgen=nextgen)
        update_board(board, nextgen, ">")

        nextgen = defaultdict(constant_factory('.'))
        move_cucumbers(board, "v",
            xmax=xmax, ymax=ymax, nextgen=nextgen)
        update_board(board, nextgen, "v")

        # print_out(gencount, board, xmax, ymax)
        if gencount == 10000:
            exit()
    print(gencount)



@timeit
def star2(data):
    ...


data2 = data[:]
star1(data)
star2(data2)