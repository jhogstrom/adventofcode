from collections import defaultdict, deque
import logging
from math import prod
from pprint import pprint
from reader import get_data, timeit, set_logging

runtest = False
stardate = "8"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]

class Node:
    def __init__(self, s) -> None:
        s, children = [_.strip() for _ in s.split("=")]
        self.children = children[1:-1].split(", ")
        self.name = s

    def __repr__(self) -> str:
        return f"{self.name}  - {self.children} {self.is_end()}"

    def is_end(self):
        return self.name[2] == "Z"


@timeit
def star1(data):
    logging.debug("running star 1")
    instructions = data[0]
    nodes = [Node(_) for _ in data[2:]]
    nodes = {_.name: _ for _ in nodes}
    p = nodes["AAA"]
    steps = 0
    while True:
        s = instructions[steps % len(instructions)]
        logging.debug(f"{steps:3}: {s} {p}")
        if s == "L":
            p = nodes[p.children[0]]
        elif s == "R":
            p = nodes[p.children[1]]
        else:
            raise ValueError
        steps += 1
        if p.name == "ZZZ":
            break
    print(steps)


def find_period(p, nodes, instructions):
    steps = 0
    is_second_end = True
    offset = 0
    period = 0
    while True:
        for s in instructions:
            if s == "L":
                p = nodes[p.children[0]]
            elif s == "R":
                p = nodes[p.children[1]]
            else:
                raise ValueError
        steps += len(instructions)
        period += 1
        # print(period, steps, p)
        if p.is_end():
            if not is_second_end:
                offset = steps
                is_second_end = True
            else:
                # print("Done", offset, steps)
                return steps, offset, period

@timeit
def star2(data):
    logging.debug("running star 2")
    instructions = data[0]
    nodes = [Node(_) for _ in data[2:]]
    nodes = {_.name: _ for _ in nodes}
    all_p = [_ for _ in nodes.values() if _.name[2] == "A"]
    data = {}
    res = []
    for i, p in enumerate(all_p):
        data[p] = find_period(p, nodes, instructions)
        res.append(data[p])

    # pprint(data)
    print(res)
    offset = sum([_[1] for _ in res])
    period = prod([_[0] / len(instructions) for _ in res])
    print(offset, period, offset+period)
    print(prod([_[2] for _ in res]) * len(instructions))
    exit()
    # logging.debug(f"{steps:3}: {p}")
    # while True:
    #     s = instructions[steps % len(instructions)]
    #     new_p = []
    #     for p in all_p:
    #         if s == "L":
    #             new_p.append(nodes[p.children[0]])
    #         elif s == "R":
    #             new_p.append(nodes[p.children[1]])
    #         else:
    #             raise ValueError
    #     steps += 1
    #     all_p = new_p
    #     # print(steps)
    #     # pprint(all_p)
    #     if all([_.is_end() for _ in all_p]):
    #         break
    #     if steps % 1_000_000 == 0:
    #         print(steps)
    # print(steps)



# star1(data)
star2(data2)
