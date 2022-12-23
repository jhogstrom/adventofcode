import os

runtest = False
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

    def traverse_edge(self, edges):
        c = (self.p, self.d)
        if c in edges:
            if self.nodes[edges[c][0]] != "#":
                self.p = edges[c][0]
                self.d = edges[c][1]
            return True
        return False

    def move_right(self, edges):
        if self.traverse_edge(edges):
            return self.p
        res = (self.p[0] + 1, self.p[1])
        if not self.nodes.get(res):
            res = (self.minx[self.p[1]], self.p[1])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_left(self, edges):
        if self.traverse_edge(edges):
            return self.p
        res = (self.p[0] - 1, self.p[1])
        if not self.nodes.get(res):
            res = (self.maxx[self.p[1]], self.p[1])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_up(self, edges):
        if self.traverse_edge(edges):
            return self.p
        res = (self.p[0], self.p[1] - 1)
        if not self.nodes.get(res):
            res = (self.p[0], self.maxy[self.p[0]])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move_down(self, edges):
        if self.traverse_edge(edges):
            return self.p
        res = (self.p[0], self.p[1] + 1)
        if not self.nodes.get(res):
            res = (self.p[0], self.miny[self.p[0]])
        if self.nodes[res] == "#":
            return self.p
        return res

    def move(self, dist, edges):
        moves = {
            0: self.move_right,
            1: self.move_down,
            2: self.move_left,
            3: self.move_up
        }
        for _ in range(dist):
            self.p = moves[self.d](edges)
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

    def extract_plane(self, w, left, top):
        res = {}
        for y in range(w*top+1, w*top+w+1):
            for x in range(w*left+1, w*left+w+1):
                res[(x, y)] = self.nodes[(x, y)]
        return res


def parse(data):
    m = Map()
    for y, line in enumerate(data[:-2], 1):
        for x, c in enumerate(line, 1):
            if c != " ":
                m.add_node(x, y, c)

    return m, data[-1]


def toprow(plane):
    my = min(_[1] for _ in plane)
    mx = min(_[0] for _ in plane)
    max_x = max(_[0] for _ in plane)
    return [(_, my) for _ in range(mx, max_x+1)]


def bottomrow(plane):
    max_y = max(_[1] for _ in plane)
    mx = min(_[0] for _ in plane)
    max_x = max(_[0] for _ in plane)
    return [(_, max_y) for _ in range(mx, max_x+1)]


def leftcol(plane):
    my = min(_[1] for _ in plane)
    max_y = max(_[1] for _ in plane)
    mx = min(_[0] for _ in plane)
    return [(mx, _) for _ in range(my, max_y+1)]


def rightcol(plane):
    my = min(_[1] for _ in plane)
    max_y = max(_[1] for _ in plane)
    max_x = max(_[0] for _ in plane)
    return [(max_x, _) for _ in range(my, max_y+1)]


def connect(source, sourcedir, target, targetdir):
    res = {}
    for i, _ in enumerate(source):
        res[(_, sourcedir)] = (target[i], targetdir)
    return res


def star2():
    m, instr = parse(data)
    m.get_start()
    # print(p, instr)
    edges = {}
    d = {
        ">": 0,
        "v": 1,
        "<": 2,
        "^": 3,
    }

    if runtest:
        w = 4
        p1 = m.extract_plane(w, 2, 0)
        p2 = m.extract_plane(w, 0, 1)
        p3 = m.extract_plane(w, 1, 1)
        p4 = m.extract_plane(w, 2, 1)
        p5 = m.extract_plane(w, 2, 2)
        p6 = m.extract_plane(w, 3, 2)
        # from p1 (top)
        edges.update(connect(toprow(p1), d["^"], toprow(p2)[::-1], d["v"]))
        edges.update(connect(rightcol(p1), d[">"], rightcol(p6)[::-1], d["<"]))
        edges.update(connect(bottomrow(p1), d["v"], toprow(p4), d["v"]))
        edges.update(connect(leftcol(p1), d["<"], toprow(p3), d["v"]))

        # from p2 (back)
        edges.update(connect(toprow(p2), d["^"], toprow(p1)[::-1], d["v"]))
        edges.update(connect(rightcol(p2), d[">"], leftcol(p3), d[">"]))
        edges.update(connect(bottomrow(p2), d["v"], bottomrow(p5)[::-1], d["v"]))
        edges.update(connect(leftcol(p2), d["<"], bottomrow(p6), d["^"]))

        # from p3 (left)
        edges.update(connect(toprow(p3), d["^"], leftcol(p1), d[">"]))
        edges.update(connect(rightcol(p3), d[">"], leftcol(p4), d[">"]))
        edges.update(connect(bottomrow(p3), d["v"], leftcol(p5)[::-1], d["v"]))
        edges.update(connect(leftcol(p3), d["<"], rightcol(p2), d["<"]))

        # from p4 (front)
        edges.update(connect(toprow(p4), d["^"], bottomrow(p1), d["^"]))
        edges.update(connect(rightcol(p4), d[">"], toprow(p6)[::-1], d["v"]))
        edges.update(connect(bottomrow(p4), d["v"], toprow(p5), d["v"]))
        edges.update(connect(leftcol(p4), d["<"], rightcol(p3), d["<"]))

        # from p6 (right)
        edges.update(connect(toprow(p6), d["^"], rightcol(p4)[::-1], d["<"]))
        edges.update(connect(rightcol(p6), d[">"], rightcol(p1)[::-1], d["<"]))
        edges.update(connect(bottomrow(p6), d["v"], leftcol(p2)[::-1], d[">"]))
        edges.update(connect(leftcol(p6), d["<"], rightcol(p5), d["<"]))

        # from p5 (bottom)
        edges.update(connect(toprow(p5), d["^"], bottomrow(p4), d["^"]))
        edges.update(connect(rightcol(p5), d[">"], rightcol(p6), d[">"]))
        edges.update(connect(bottomrow(p5), d["v"], bottomrow(p2)[::-1], d["^"]))
        edges.update(connect(leftcol(p5), d["<"], bottomrow(p3)[::-1], d["^"]))
    else:
        w = 50
        p1 = m.extract_plane(w, 1, 0)
        p2 = m.extract_plane(w, 2, 0)
        p3 = m.extract_plane(w, 1, 1)
        p4 = m.extract_plane(w, 0, 2)
        p5 = m.extract_plane(w, 1, 2)
        p6 = m.extract_plane(w, 0, 3)

        # from p1
        edges.update(connect(toprow(p1), d["^"], leftcol(p6), d[">"]))
        edges.update(connect(rightcol(p1), d[">"], leftcol(p2), d[">"]))
        edges.update(connect(bottomrow(p1), d["v"], toprow(p3), d["v"]))
        edges.update(connect(leftcol(p1), d["<"], leftcol(p4)[::-1], d[">"]))

        # from p2
        edges.update(connect(toprow(p2), d["^"], bottomrow(p6), d["^"]))
        edges.update(connect(rightcol(p2), d[">"], rightcol(p5)[::-1], d["<"]))
        edges.update(connect(bottomrow(p2), d["v"], rightcol(p3), d["<"]))
        edges.update(connect(leftcol(p2), d["<"], rightcol(p1), d["<"]))

        # from p3
        edges.update(connect(toprow(p3), d["^"], bottomrow(p1), d["^"]))
        edges.update(connect(rightcol(p3), d[">"], bottomrow(p2), d["^"]))
        edges.update(connect(bottomrow(p3), d["v"], toprow(p5), d["v"]))
        edges.update(connect(leftcol(p3), d["<"], toprow(p4), d["v"]))

        # from p4
        edges.update(connect(toprow(p4), d["^"], leftcol(p3), d[">"]))
        edges.update(connect(rightcol(p4), d[">"], leftcol(p5), d[">"]))
        edges.update(connect(bottomrow(p4), d["v"], toprow(p6), d["v"]))
        edges.update(connect(leftcol(p4), d["<"], leftcol(p1)[::-1], d[">"]))

        # from p6
        edges.update(connect(toprow(p6), d["^"], bottomrow(p4), d["^"]))
        edges.update(connect(rightcol(p6), d[">"], bottomrow(p5), d["^"]))
        edges.update(connect(bottomrow(p6), d["v"], toprow(p2), d["v"]))
        edges.update(connect(leftcol(p6), d["<"], toprow(p1), d["v"]))

        # from p5
        edges.update(connect(toprow(p5), d["^"], bottomrow(p3), d["^"]))
        edges.update(connect(rightcol(p5), d[">"], rightcol(p2)[::-1], d["<"]))
        edges.update(connect(bottomrow(p5), d["v"], rightcol(p6), d["<"]))
        edges.update(connect(leftcol(p5), d["<"], rightcol(p4), d["<"]))

    res = ""
    for _ in instr:
        res += _
        if _ in "RL":
            m.move(int(res[:-1]), edges)
            m.turn(res[-1])
            res = ""
    if res:
        m.move(int(res), edges)
    # m.print()
    return 1000 * m.p[1] + 4 * m.p[0] + m.d


print("star2:", star2())
