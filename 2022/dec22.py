import os

runtest = True
stardate = 22
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Map():
    def __init__(self) -> None:
        self.nodes = {}
        self.d = 0
        self.miny = {}
        self.maxy = {}
        self.minx = {}
        self.maxx = {}
        self.path = {}
        self.dirs = ">v<^"

    def add_node(self, x, y, c):
        self.nodes[(x, y)] = c
        self.minx[y] = min([x, self.minx.get(y, 999999)])
        self.maxx[y] = max([x, self.maxx.get(y, 0)])
        self.miny[x] = min([y, self.miny.get(x, 999999)])
        self.maxy[x] = max([y, self.maxy.get(x, 0)])

    def get_start(self):
        x = 0
        while self.nodes.get((x, 1), "#") != '.':
            x += 1
        self.p = (x, 1)
        self.path[(self.p)] = self.dirs[self.d]
        return (x, 1)

    def move_right(self):
        res = (self.p[0] + 1, self.p[1])
        if not self.nodes.get(res):
            res = (self.minx[self.p[1]], self.p[1])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_left(self):
        res = (self.p[0] - 1, self.p[1])
        if not self.nodes.get(res):
            res = (self.maxx[self.p[1]], self.p[1])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_up(self):
        res = (self.p[0], self.p[1] - 1)
        if not self.nodes.get(res):
            res = (self.p[0], self.maxy[self.p[0]])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_down(self):
        res = (self.p[0], self.p[1] + 1)
        if not self.nodes.get(res):
            res = (self.p[0], self.miny[self.p[0]])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move(self, dist):
        moves = {
            0: self.move_right,
            1: self.move_down,
            2: self.move_left,
            3: self.move_up
        }
        for _ in range(dist):
            self.p = moves[self.d]()
            self.path[(self.p)] = self.dirs[self.d]

    def turn(self, d):
        self.d += 1 if d == "R" else -1
        self.d %= 4
        self.path[(self.p)] = self.dirs[self.d]

    def print(self):
        for y in range(min(self.miny.values()), max(self.maxy.values()), 1):
            res = ""
            for x in range(min(self.minx.values()), max(self.maxx.values()), 1):
                if self.path.get((x, y)):
                    res += self.path.get((x, y))
                else:
                    res += self.nodes.get((x, y), " ")
            print(res)


def parse(data):
    m = Map()
    for y, line in enumerate(data[:-2], 1):
        for x, c in enumerate(line, 1):
            if c != " ":
                m.add_node(x, y, c)

    return m, data[-1]


def star1():
    m, instr = parse(data)
    p = m.get_start()
    print(p, instr)

    res = ""
    for _ in instr:
        res += _
        if _ in "RL":
            m.move(int(res[:-1]))
            m.turn(res[-1])
            res = ""
    if res:
        m.move(int(res))
    # m.print()
    return 1000 * m.p[1] + 4 * m.p[0] + m.d


print("star1:", star1())
