import os
from typing import List
from timer import timeit
from collections import defaultdict, deque

stardate = 12
dataname = f"dec{stardate}.txt"
dataname = f"dec{stardate}_test1.txt" # star1/star2: 10/36
# dataname = f"dec{stardate}_test.txt" # star1/star2: 19/103
# dataname = f"dec{stardate}_test2.txt" # star1/star2: 226/3509
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip().split("-") for _ in open(filename, 'r').readlines()]

class Node():
    def __init__(self, start) -> None:
        self.start = start
        self.next: List[Node] = []

    def add_next(self, nodes):
        self.next.extend(nodes)

    @property
    def is_small(self):
        return (self.start != self.start.upper())

def check_star2(trail: List[Node], node: Node) -> bool:
    counter = defaultdict(int)
    for t in trail + [node]:
        if t.is_small:
            counter[t.start] += 1

    visits = list(counter.values()) + [0]
    res = max(visits) <= 2 and visits.count(2) <= 1
    return res

def check_star1(trail: List[Node], node: Node) -> bool:
    return node not in trail

def traverse(start: Node, target, trail: List[Node], check):
    res = 0
    if start.start == target:
        print(" - ".join(_.start for _ in trail))
        return 1
    for n in (_ for _ in start.next if _.start != "start"):
        if not n.is_small or check(trail, n):
            res += traverse(n, target, trail + [n], check)

    return res


def make_nodes(data) -> List[Node]:
    nodes = []
    for d in data:
        if not any(_ for _ in nodes if _.start == d[0]):
            nodes.append(Node(d[0]))
        if not any(_ for _ in nodes if _.start == d[1]):
            nodes.append(Node(d[1]))

    for d in data:
        start = [_ for _ in nodes if _.start == d[0]]
        end = [_ for _ in nodes if _.start == d[1]]
        start[0].add_next(end)
        if len(end) == 1:
            end[0].add_next(start)

    # for n in nodes:
    #     print(n)
    # print("===")
    start = [_ for _ in nodes if _.start == "start"][0]
    return start


@timeit
def star1(start):
    print(traverse(start, "end", [start], check_star1))


@timeit
def star2(start):
    print(traverse(start, "end", [start], check_star2))


start = make_nodes(data)

star1(start)
star2(start)
