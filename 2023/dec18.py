from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "18"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]

moves = {
    "R": lambda p: (p[0]+1, p[1]),
    "L": lambda p: (p[0]-1, p[1]),
    "U": lambda p: (p[0], p[1]-1),
    "D": lambda p: (p[0], p[1]+1),
}


@timeit
def star1(data):
    logging.debug("running star 1")
    p = (0, 0)
    frame = {p}

    for instr in data:
        d, length, _ = instr.split()
        length = int(length)
        for _ in range(length):
            p = moves[d](p)
            frame.add(p)

    filled = 0
    for y in range(min([_[1] for _ in frame]), max([_[1] for _ in frame])+1):
        inside = False
        turns = []
        for x in range(min([_[0] for _ in frame]), max([_[0] for _ in frame])+1):
            if (x, y) in frame:
                filled += 1
                if (x, y-1) in frame:
                    turns.append("UP")
                if (x, y+1) in frame:
                    turns.append("DOWN")
                if len(turns) == 2 and (x+1, y) not in frame:
                    if "UP" in turns and "DOWN" in turns:
                        inside = not inside
                    turns = []
                    # print("X", end="")
                # else:
                #     print("#", end="")
            else:
                if inside:
                    filled += 1
                #     print(".", end="")
                # else:
                #     print(" ", end="")
        # print()
    print(filled)


@timeit
def star2(data):
    logging.debug("running star 2")
    p = (0, 0)
    corners = [p]
    framelen = 0
    for instr in data:
        _, _, i = instr.split()
        length = int(i[2:-2], 16)
        d = "RDLU"[int(i[-2])]
        if d == "R":
            p = (p[0]+length, p[1])
        elif d == "L":
            p = (p[0]-length, p[1])
        elif d == "U":
            p = (p[0], p[1]-length)
        elif d == "D":
            p = (p[0], p[1]+length)
        corners.append(p)
        framelen += length
    area = sum([(corners[k+1][0] + p[0]) * (corners[k+1][1] - p[1]) / 2 for k, p in enumerate(corners[:-1])])
    area = int(area + (framelen)/2 + 1)
    print(area)


star1(data)
star2(data2)
