from collections import defaultdict
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "15"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)


def calc_hash(string):
    res = 0
    for c in string:
        res += ord(c)
        res *= 17
        res %= 256
    return res


@timeit
def star1(data):
    logging.debug("running star 1")
    res = sum([calc_hash(_) for _ in data[0].split(",")])
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    strings = data[0].split(",")
    boxes = defaultdict(dict)
    boxlabels = defaultdict(list)
    for s in strings:
        if "=" in s:
            lbl, val, cmd = s.split("=") + ["="]
        else:
            lbl, val, cmd = s.split("-") + ["-"]
        box = calc_hash(lbl)
        if cmd == "-":
            boxes[box].pop(lbl, 0)
            if lbl in boxlabels[box]:
                boxlabels[box].remove(lbl)
        else:
            boxes[box][lbl] = int(val)
            if lbl not in boxlabels[box]:
                boxlabels[box].append(lbl)

    res = 0
    for box in boxes:
        for slot, lens in enumerate(boxlabels[box], 1):
            fp = (box+1) * slot * boxes[box][lens]
            # print(f"{lens}: {box+1} * {slot} * {boxes[box][lens]} = {fp}")
            res += fp

    print(res)


star1(data)
star2(data)
