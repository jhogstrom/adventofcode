import logging
from typing import List

from reader import get_data, set_logging, timeit

runtest = False
stardate = "04"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def print_xmas(data, path):
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if (x, y) in path:
                print(c, end="")
            else:
                print(".", end="")
        print()


def search(
    x: int, y: int, s: str, data, path: List, dir_x: List[int], dir_y: List[int]
) -> int:
    dir_x = dir_x or [-1, 0, 1]
    dir_y = dir_y or [-1, 0, 1]
    if not s:
        return 1

    result = 0
    for dx in dir_x:
        for dy in dir_y:
            if (
                x + dx < 0
                or y + dy < 0
                or x + dx >= len(data[0])
                or y + dy >= len(data)
            ):
                continue
            if data[y + dy][x + dx] == s[0]:
                result += search(
                    x + dx,
                    y + dy,
                    s[1:],
                    data,
                    # result,
                    path + [(x + dx, y + dy)],
                    dir_x=[dx],
                    dir_y=[dy],
                )
    return result


@timeit
def star1(data):
    logging.debug("running star 1")
    result = 0
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c == "X":
                r = search(
                    x=x, y=y, s="MAS", data=data, path=[(x, y)], dir_x=[], dir_y=[]
                )
                result += r
    print(result)


def is_xmas(x, y, data):
    ne = (x - 1, y - 1)
    nw = (x + 1, y - 1)
    se = (x - 1, y + 1)
    sw = (x + 1, y + 1)

    for x, y in [ne, nw, se, sw]:
        if x < 0 or y < 0 or x >= len(data[0]) or y >= len(data):
            return False

    top = data[ne[1]][ne[0]] + data[nw[1]][nw[0]]
    bottom = data[se[1]][se[0]] + data[sw[1]][sw[0]]

    if top == "MM" and bottom == "SS":
        return True
    if top == "SS" and bottom == "MM":
        return True
    if top == "MS" and bottom == "MS":
        return True
    if top == "SM" and bottom == "SM":
        return True
    return False


@timeit
def star2(data):
    logging.debug("running star 2")
    result = 0
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if c == "A":
                if is_xmas(x, y, data):
                    result += 1
    print(result)


star1(data)
star2(data2)
