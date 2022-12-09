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


def count_smaller(tree, trees) -> int:
    res = 0
    for _ in trees:
        res += 1
        if tree <= _:
            return res
    return res


def star():
    star1 = 2 * len(data[0]) + 2 * len(data) - 4
    star2 = 0
    for x in range(1, len(data[0])-1):
        for y in range(1, len(data)-1):
            istallest, viewscore = False, 1
            tree = data[y][x]

            # left
            line = data[y][:x][::-1]
            istallest |= tallest(tree, line)
            viewscore *= count_smaller(tree, line)

            # right
            line = data[y][x+1:]
            istallest |= tallest(tree, line)
            viewscore *= count_smaller(tree, line)

            # up
            line = get_topmost(data, x, y)[::-1]
            istallest |= tallest(tree, line)
            viewscore *= count_smaller(tree, line)

            # down
            line = get_bottommost(data, x, y)
            istallest |= tallest(tree, line)
            viewscore *= count_smaller(tree, line)
            if istallest:
                star1 += 1
            star2 = max([star2, viewscore])
    print("star1", star1)
    print("star2", star2)


star()
