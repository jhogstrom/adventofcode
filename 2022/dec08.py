import os

runtest = False
stardate = "08"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


def tallest(tree, trees) -> bool:
    return trees and all([tree > _ for _ in trees])


def get_topmost(data, x, y) -> str:
    res = ""
    for _ in range(y):
        res += data[_][x]
    # print(x, _, res)
    return res


def get_bottommost(data, x, y) -> str:
    res = ""
    for _ in range(y+1, len(data)):
        res += data[_][x]
    # print(x, _, res)
    return res


def debug(s):
    # print(s)
    pass


def star1():
    res = 2 * len(data[0]) + 2 * len(data) - 4
    for x in range(1, len(data[0])-1) :
        for y in range(1, len(data)-1):
            tree = data[y][x]
            line = data[y][:x]
            if tallest(tree, line):
                res += 1
                debug(f"from left {tree} {line}, {data[y]}")
                continue

            line = data[y][x+1:]
            if tallest(tree, line):
                res += 1
                debug(f"from right {tree} {line}, {data[y]}")
                continue

            line = get_topmost(data, x, y)
            if tallest(tree, line):
                res += 1
                debug(f"from top {tree} {line}, {data[y]}")
                continue

            line = get_bottommost(data, x, y)
            if tallest(tree, line):
                res += 1
                debug(f"from bottom {tree} {line}, {data[y]}")
                continue
    return res


def count_smaller(tree, trees) -> int:
    res = 0
    for _ in trees:
        res += 1
        if tree <= _:
            return res
    return res


def star2():
    res = 0
    for x in range(1, len(data[0])-1) :
        for y in range(1, len(data)-1):
            tree = data[y][x]
            line = data[y][:x][::-1]
            look_left = count_smaller(tree, line)
            debug(f"left : {tree}: {line} -> {look_left}")

            line = data[y][x+1:]
            look_right = count_smaller(tree, line)
            debug(f"right: {tree}: {line} -> {look_right}")

            line = get_topmost(data, x, y)[::-1]
            look_up = count_smaller(tree, line)
            debug(f"up   : {tree}: {line} -> {look_up}")

            line = get_bottommost(data, x, y)
            look_down = count_smaller(tree, line)
            debug(f"down : {tree}: {line} -> {look_down}")

            score = look_down*look_up*look_right*look_left
            # if score > res:
            #     print(f"({x+1}, {y+1}): {tree} -> {score} ({look_up}, {look_right}, {look_down}, {look_left})")
            res = max([res, score])

    return res


print("star1:", star1())
print("star2:", star2())
