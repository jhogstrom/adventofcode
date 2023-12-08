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
        p = nodes[p.children[0 if s == "L" else 1]]
        steps += 1
        if p.name == "ZZZ":
            break
    print(steps)


def find_period(p, nodes, instructions):
    period = 0
    while not p.is_end():
        for s in instructions:
            p = nodes[p.children[0 if s == "L" else 1]]
        period += 1
    return period


@timeit
def star2(data):
    logging.debug("running star 2")
    instructions = data[0]
    nodes = [Node(_) for _ in data[2:]]
    nodes = {_.name: _ for _ in nodes}
    all_p = [_ for _ in nodes.values() if _.name[2] == "A"]
    res = [find_period(p, nodes, instructions) for p in all_p]

    print(prod(res) * len(instructions))


star1(data)
star2(data2)
