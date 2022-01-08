import os
from typing import List
from timer import timeit
from collections import defaultdict, deque

stardate = 12
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test1.txt" # star1/star2: 10/36
# dataname = f"dec{stardate}_test.txt" # star1/star2: 19/103
# dataname = f"dec{stardate}_test2.txt" # star1/star2: 226/3509
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip().split("-") for _ in open(filename, 'r').readlines()]

class Node():
    def __init__(self, node_name) -> None:
        self.node_name = node_name
        self.next: List[Node] = []
        self.is_small = self.node_name != self.node_name.upper()
        self.is_start = node_name == "start"

    def add_next(self, nodes):
        self.next.extend(nodes)


def check_star2(trail: List[Node], node: Node) -> bool:
    counter = defaultdict(int)
    for t in [_ for _ in trail + [node] if _.is_small]:
        counter[t.node_name] += 1

    visits = list(counter.values())
    return max(visits) <= 2 and visits.count(2) <= 1


def check_star1(trail: List[Node], node: Node) -> bool:
    return node not in trail


def traverse(node: Node, target, trail: List[Node], check):
    res = 0
    if node.node_name == target:
        # print(" - ".join(_.start for _ in trail))
        return 1
    for n in (_ for _ in node.next if not _.is_start):
        if not n.is_small or check(trail, n):
            res += traverse(n, target, trail + [n], check)

    return res


def make_nodes(data) -> List[Node]:
    nodes = []
    for d in data:
        if not any(_ for _ in nodes if _.node_name == d[0]):
            nodes.append(Node(d[0]))
        if not any(_ for _ in nodes if _.node_name == d[1]):
            nodes.append(Node(d[1]))

    for d in data:
        start = next(_ for _ in nodes if _.node_name == d[0])
        end = [_ for _ in nodes if _.node_name == d[1]]
        start.add_next(end)
        if len(end) == 1:
            end[0].add_next([start])

    first_node = next(_ for _ in nodes if _.is_start)
    return first_node


@timeit
def star1(first_node):
    print(traverse(first_node, "end", [first_node], check_star1))


@timeit
def star2(first_node):
    print(traverse(first_node, "end", [first_node], check_star2))


first_node = make_nodes(data)

star1(first_node)
star2(first_node)
