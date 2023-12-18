import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "18"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)


def star1_instructions(data):
    res = []
    for instr in data:
        d, length, _ = instr.split()
        length = int(length)
        res.append((d, length))
    return res


def star2_instructions(data):
    res = []
    for instr in data:
        _, _, i = instr.split()
        length = int(i[2:-2], 16)
        d = "RDLU"[int(i[-2])]
        res.append((d, length))
    return res


def docalc(data, instruction_extractor):
    instructions = instruction_extractor(data)
    p = (0, 0)
    corners = [p]
    framelen = 0
    for instr in instructions:
        d, length = instr
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


@timeit
def star1(data):
    logging.debug("running star 1")
    docalc(data, star1_instructions)


@timeit
def star2(data):
    logging.debug("running star 2")
    docalc(data, star2_instructions)


star1(data)
star2(data)
