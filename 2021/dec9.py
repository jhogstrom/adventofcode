import os
from timer import timeit
from collections import defaultdict, deque

stardate = 9
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]


def is_lowest(x, y, data):
    res = True
    p = int(data[y][x])
    if y > 0:
        res &= p < int(data[y-1][x])
    if y < len(data) - 1:
        res &= p < int(data[y+1][x])
    if x > 0:
        res &= p < int(data[y][x-1])
    if x < len(data[y]) - 1:
        res &= p < int(data[y][x+1])
    return res

@timeit
def star1(data):
    lowpoints = []
    for y in range(len(data)):
        for x in range(len(data[y])):

            if is_lowest(x, y, data):
                lowpoints.append(int(data[y][x]) + 1)

    print(sum(lowpoints))


def floodfill(matrix, x, y, basin):
    if matrix[y][x] in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        basin.append(matrix[y][x])
        matrix[y][x] = 9
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(matrix, x-1, y, basin)
        if x < len(matrix[y]) - 1:
            floodfill(matrix, x+1, y, basin)
        if y > 0:
            floodfill(matrix, x, y-1, basin)
        if y < len(matrix) - 1:
            floodfill(matrix, x, y+1, basin)


@timeit
def star2(data):
    grid = []
    for y in range(len(data)):
        r = []
        for x in range(len(data[y])):
            r.append(int(data[y][x]))
        grid.append(r)

    basins = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            basin = []
            floodfill(grid, x, y, basin)
            if basin:
                basins.append(len(basin))
    res = 1
    for r in sorted(basins)[-3:]:
        res *= r
    print(res)


star1(data)
star2(data)
