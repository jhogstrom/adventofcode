import os
from timer import timeit
from collections import defaultdict, deque

stardate = 13
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")

def read_data(data):
    dots = []
    folds = []
    readdots = True
    for d in data:
        if d == "":
            readdots = False
            continue
        if readdots:
            dots.append([int(_) for _ in d.split(",")])
        else:
            folds.append(d.replace("fold along ", "").split("="))
    return dots, folds


def count_dots(dots):
    dotvals = defaultdict(int)
    for d in dots:
        p = (d[0], d[1])
        dotvals[(d[0], d[1])] = 1

    return sum(dotvals.values())


def make_fold(fold, dots):
    fold_direction = fold[0]
    foldline = int(fold[1])

    index = 1 if fold_direction == "y" else 0

    for d in dots:
        if d[index] > foldline:
            d[index] = 2 * foldline - d[index]
    return dots


def print_data(dots):
    maxy = max(_[1] for _ in dots) + 1
    lines = []
    for y in range(maxy):
        lines.append([])
    for d in dots:
        lines[d[1]].append(d[0])
    for line in lines:
        s = ""
        if line:
            for x in range(max(line) + 1):
                s += "#" if x in line else " "
        print(s)


@timeit
def star1(data):
    dots, folds = read_data(data)
    dots = make_fold(folds[0], dots)

    count = count_dots(dots)
    print("Count", count)


@timeit
def star2(data):
    dots, folds = read_data(data)
    for fold in folds:
        dots = make_fold(fold, dots)

    print_data(dots)

data2 = data[:]
star1(data)
star2(data2)