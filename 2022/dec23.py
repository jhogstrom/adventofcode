from collections import defaultdict
import os

runtest = False
stardate = 23
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Node():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return self.x == __o.x and self.y == __o.y
        return self.x == __o[0] and self.y == __o[1]

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def n_n(self):
        return {(self.x-1, self.y-1), (self.x, self.y-1), (self.x+1, self.y-1)}

    def n_s(self):
        return {(self.x-1, self.y+1), (self.x, self.y+1), (self.x+1, self.y+1)}

    def n_w(self):
        return {(self.x-1, self.y-1), (self.x-1, self.y), (self.x-1, self.y+1)}

    def n_e(self):
        return {(self.x+1, self.y-1), (self.x+1, self.y), (self.x+1, self.y+1)}

    def n_all(self):
        return self.n_n() | self.n_e() | self.n_s() | self.n_w()

    def is_occupied(self, loc, nodes):
        return any(_ in nodes for _ in loc)

    def has_neighbors(self, nodes):
        return self.is_occupied(self.n_all(), nodes)


class Map():
    def __init__(self) -> None:
        self.nodes = []
        self.box = [999, 999, 0, 0]
        self.rounds = 0

        self.checks = [
            lambda node: node.n_n(),
            lambda node: node.n_s(),
            lambda node: node.n_w(),
            lambda node: node.n_e()
        ]

        self.moves = [
            lambda node: (node.x, node.y-1),
            lambda node: (node.x, node.y+1),
            lambda node: (node.x-1, node.y),
            lambda node: (node.x+1, node.y)
        ]

    def update_box(self, n):
        self.box[0] = min([self.box[0], n.x])
        self.box[1] = min([self.box[1], n.y])
        self.box[2] = max([self.box[2], n.x+1])
        self.box[3] = max([self.box[3], n.y+1])

    def add_node(self, x, y):
        node = Node(x, y)
        self.nodes.append(node)
        self.update_box(node)

    def print(self):
        print(f"Round: {self.rounds} - Free: {self.free_nodes()} Nodes = {len(self.nodes)}")
        for y in range(self.box[1], self.box[3]):
            s = []
            for x in range(self.box[0], self.box[2]):
                s.append("#" if (x, y) in self.nodes else ".")
            print("".join(s))

    def proposals(self):
        res = defaultdict(list)
        nodes = set(self.nodes)
        for n in nodes:
            if not n.has_neighbors(nodes):
                continue

            for r in range(4):
                if not n.is_occupied(self.checks[(self.rounds + r) % 4](n), nodes):
                    res[self.moves[(self.rounds + r) % 4](n)].append(n)
                    break
        return res

    def move(self, proposals):
        for p, nodes in proposals.items():
            if len(nodes) == 1:
                nodes[0].x = p[0]
                nodes[0].y = p[1]
                self.update_box(nodes[0])

    def round(self):
        proposals = self.proposals()
        self.move(proposals)
        self.rounds += 1
        return len(proposals)

    def free_nodes(self):
        # Since the bounding box may have shrunk, shave of empy edges.
        if not any((self.box[0], y) in self.nodes for y in range(self.box[1], self.box[3])):
            self.box[0] += 1
        if not any((self.box[2]-1, y) in self.nodes for y in range(self.box[1], self.box[3])):
            self.box[2] -= 1
        if not any((x, self.box[1]) in self.nodes for x in range(self.box[0], self.box[2])):
            self.box[1] += 1
        if not any((x, self.box[3]-1) in self.nodes for x in range(self.box[0], self.box[2])):
            self.box[3] -= 1
        return (self.box[2]-self.box[0]) * (self.box[3]-self.box[1]) - len(self.nodes)


def parse(data):
    res = Map()
    for y, ly in enumerate(data):
        for x, cx in enumerate(ly):
            if cx == "#":
                res.add_node(x, y)
    return res


def star1():
    m = parse(data)
    for _ in range(10):
        m.round()
    return m.free_nodes()


def star2():
    m = parse(data)
    while True:
        r = m.round()
        print(m.rounds, r, end="\r")
        if r == 0:
            return m.rounds


print("star1:", star1())
print("star2:", star2())
