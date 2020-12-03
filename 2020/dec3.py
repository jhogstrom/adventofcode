import os
import itertools
import time
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec3.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
#     "..##.......",
#     "#...#...#..",
#     ".#....#..#.",
#     "..#.#...#.#",
#     ".#...##..#.",
#     "..#.##.....",
#     ".#.#.#....#",
#     ".#........#",
#     "#.##...#...",
#     "#...##....#",
#     ".#..#...#.#"
#     ]

def counttrees(dx, dy):
    y = x = trees = 0
    while y < len(data):
        cell = data[y][x % len(data[y])]
        trees += int(cell == "#")
        y += dy
        x += dx
    return trees

def star1():
    print(counttrees(3, 1))

def star2():
    p1 = counttrees(1, 1)
    p2 = counttrees(3, 1)
    p3 = counttrees(5, 1)
    p4 = counttrees(7, 1)
    p5 = counttrees(1, 2)
    print(p1*p2*p3*p4*p5)

star1()
star2()