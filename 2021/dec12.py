import os
from typing import List
from timer import timeit
from collections import defaultdict, deque

stardate = 12
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test1.txt" # star1/star2: 10/36
# dataname = f"dec{stardate}_test.txt" # star1/star2: 19/103
# dataname = f"dec{stardate}_test2.txt" # star1/star2: 226/
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
    def is_large(self):
        return (self.start == self.start.upper()) or (self.start in ["start", "end"])

    @property
    def is_small(self):
        return not self.is_large

    def __str__(self) -> str:
        nextnodes = [_.start for _ in self.next]
        n = ", ".join(nextnodes)
        return f"{self.start} -> {n}"

def path(visited: List[Node]):
    res = []
    for n in visited:
        res.append(n.start)
    return " - ".join(res)

count = 0

def can_reach(start: Node, target, trail: List[Node]):
    global count
    tabs = "  " * trail.count(",")
    # print(f"{tabs}Examining '{start.start}' (from {trail}) (Next: {path(start.next)})")
    if start.start == target:
        print(f"** Found target: {path(trail)}")
        count += 1
        return True
    for n in [_ for _ in start.next if _.start != "start"]:
        if n.is_large or (n.is_small and n not in trail):
            # print(f"Leaving {start.start}")
            can_reach(n, target, trail + [n])
        # else:
        #     print(f"{tabs}Will not visit {n.start} from {start.start}")


    # print(f"Couldn't find target from {start.start}")
    return False


def may_visit(trail: List[Node], node: Node) -> int:
    if node.start == "start":
        return False
    counter = defaultdict(int)
    for t in trail:
        if t.is_small:
            counter[t.start] += 1

    visits = list(counter.values()) + [0]
    res = max(visits) <= 2 and visits.count(2) <= 1
    # if res:
    #     print(max(visits), visits)

    return res

def can_reach2(start: Node, target, trail: List[Node]):
    # print("CAN2")
    global count
    tabs = "  " * trail.count(",")
    # print(f"{tabs}Examining '{start.start}' (from {trail}) (Next: {path(start.next)})")
    if start.start == target:
        # print(f"** Found target: {path(trail)}")
        count += 1
        return True
    for n in [_ for _ in start.next if _.start != "start"]:
        if n.is_large or (n.is_small and may_visit(trail + [n], n)):
            # print(f"Leaving {start.start}")
            can_reach2(n, target, trail + [n])
        # else:
        #     print(f"{tabs}Will not visit {n.start} from {start.start}")


    # print(f"Couldn't find target from {start.start}")
    return False


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

    for n in nodes:
        print(n)
    print("===")
    start = [_ for _ in nodes if _.start == "start"][0]
    return start

@timeit
def star1(data):
    start = make_nodes(data)
    can_reach(start, "end", [start])
    print(count)


@timeit
def star2(data):
    start = make_nodes(data)
    print(start.is_small)
    can_reach2(start, "end", [start])
    print(count)

data2 = data[:]

# star1(data)
count = 0
star2(data2)