from computer import intcomputer
from cell import Cell
import os

def get_char(c):
    CHARS = " XB_*"
    if c < len(CHARS):
        return CHARS[c]
    return "O"
    raise Exception(f"Attempted to get {c}")

def print_grid(grid):
    y_vals = [_.y for _ in grid]
    x_vals = [_.x for _ in grid]
    for y in range(min(y_vals), max(y_vals)+1):
        for x in range(min(x_vals), max(x_vals)+1):
            c = Cell(x, y)
            if c in grid:
                print(get_char(grid[c]), end = "")
            else:
                print("_", end = "")
        print()


def dec13_star1():
    curdir = os.path.dirname(os.path.abspath(__file__))
    filename = f'{curdir}\\dec13.txt'
    prgdata = [int(_) for _ in open(filename, 'r').readline().split(",")]
    c = intcomputer(prgdata, param_array=[]).execute()
    blocktiles = len([_ for _ in c.outputarray[2::3] if _ == 2])
    print("Answer: ", blocktiles)

def blockcount(grid):
    return len([_ for _ in grid if grid[_] == 2])

def get_ball_pos(grid):
    return [_ for _ in grid if grid[_] == 4][0]

def get_paddle_pos(grid):
    return [_ for _ in grid if grid[_] == 3][0]

def move_paddle(ball, paddle):
    if paddle.x == ball.x:
        return 0
    if paddle.x > ball.x:
        return -1
    return 1

def make_grid(res):
    grid = {}
    for i in range(0, len(res), 3):
        grid[Cell(res[i], res[i+1])] = res[i+2]
    return grid


def dec13_star2():
    curdir = os.path.dirname(os.path.abspath(__file__))
    filename = f'{curdir}\\dec13.txt'
    prgdata = [int(_) for _ in open(filename, 'r').readline().split(",")]
    prgdata[0] = 2

    scorecell = Cell(-1, 0)
    c = intcomputer(prgdata, param_array=[])
    grid = make_grid(c.execute().outputarray)
    while blockcount(grid) > 0 and not c._terminated:
        ball = get_ball_pos(grid)
        paddle = get_paddle_pos(grid)
        c.add_input(move_paddle(ball, paddle))
        if scorecell in grid:
            print(f"score: {grid[scorecell]}")
        grid = make_grid(c.execute().outputarray)
        print_grid(grid)
    
    print(grid[Cell(-1, 0)])

dec13_star2()
