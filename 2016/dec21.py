import logging

# from collections import defaultdict, deque
# from pprint import pprint
from typing import List  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "21"
year = "2016"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data, pwd: str):
    logging.debug("running star 1")
    pwd = list(pwd)
    steps = []
    for line in data:
        verb, *args = line.split()
        if verb == "swap":
            if args[0] == "position":
                a, b = int(args[1]), int(args[-1])
                pwd[a], pwd[b] = pwd[b], pwd[a]
            else:
                a, b = args[1], args[-1]
                a, b = pwd.index(a), pwd.index(b)
                pwd[a], pwd[b] = pwd[b], pwd[a]
        elif verb == "rotate":
            if args[0] == "left":
                pwd = rotate_left(pwd, int(args[1]))
            elif args[0] == "right":
                pwd = rotate_right(pwd, int(args[1]))
            else:
                pwd = rotate_by_char(pwd, args[-1])
        elif verb == "reverse":
            a, b = int(args[1]), int(args[-1])
            pwd = pwd[:a] + pwd[a : b + 1][::-1] + pwd[b + 1 :]  # noqa e203
        elif verb == "move":
            a, b = int(args[1]), int(args[-1])
            c = pwd[a]
            pwd = pwd[:a] + pwd[a + 1 :]  # noqa e203
            pwd = pwd[:b] + [c] + pwd[b:]
        steps.append("".join(pwd))
        print("".join(pwd), line)
    print("".join(pwd))
    if steps[-1] != "gfdhebac":
        print("not found")
    return steps


def rotate_by_char(pwd, ch):
    a = pwd.index(ch)
    if a >= 4:
        a += 1
    a += 1
    a %= len(pwd)
    return pwd[-a:] + pwd[:-a]


def rotate_right(pwd, shift):
    return pwd[-shift:] + pwd[:-shift]


def rotate_left(pwd, shift):
    return pwd[shift:] + pwd[:shift]


@timeit
def star2(data, steps: List[str]):
    logging.debug("running star 2")
    pwd = list("fbgdceah")
    # print(steps)
    rev_rotate = {
        "".join(rotate_by_char(list("_" * i + "h" + "_" * (7 - i)), "h")).index("h"): i
        for i in range(8)
    }
    print("".join(pwd))
    for line, step in zip(data[::-1], steps[::-1]):
        verb, *args = line.split()
        if verb == "swap":
            if args[0] == "position":
                a, b = int(args[1]), int(args[-1])
                pwd[a], pwd[b] = pwd[b], pwd[a]
            else:
                a, b = args[1], args[-1]
                a, b = pwd.index(a), pwd.index(b)
                pwd[a], pwd[b] = pwd[b], pwd[a]
        elif verb == "rotate":
            if args[0] == "right":
                pwd = rotate_left(pwd, int(args[1]))
            elif args[0] == "left":
                pwd = rotate_right(pwd, int(args[1]))
            else:
                p = pwd.index(args[-1])
                pwd = rotate_left(pwd, p - rev_rotate[p])
        elif verb == "reverse":
            a, b = int(args[1]), int(args[-1])
            pwd = pwd[:a] + pwd[a : b + 1][::-1] + pwd[b + 1 :]  # noqa e203
        elif verb == "move":
            b, a = int(args[1]), int(args[-1])
            c = pwd[a]
            pwd = pwd[:a] + pwd[a + 1 :]  # noqa e203
            pwd = pwd[:b] + [c] + pwd[b:]
        print("".join(pwd), step, line)
        # if step != "".join(pwd):
        #     break
    print("".join(pwd))


# for i in range(8):
#     p = "_" * i + "h" + "_" * (7 - i)
#     print(p, "".join(rotate_by_char(list(p), "h")))

steps = star1(data, "abcdefgh")
star2(data2, steps[:])
