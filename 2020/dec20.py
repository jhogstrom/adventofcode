import helpers
from itertools import permutations
import math
from timing import timeit

extra = "_demo"
extra = ""
data = helpers.get_data(__file__, extra=extra)

data = helpers.get_records(data)

class Tile():
    def __init__(self, arr):
        self.number = arr[0][5:-1]
        self.tile = arr[1:]
        self.rotations = self.make_rotations()
        self.neighbors = set()
        self.all_edges = self.get_all_edges()
        self.rotation = 0

        self.unique_edges = set()
        for r in self.all_edges:
            self.unique_edges |= set(r)

    def rotate_tile(self, tile=None):
        mod = tile is None
        tile = tile or self.tile.copy()
        res = []
        for x in range(len(tile[0])-1, -1, -1):
            line = []
            for y in range(len(tile)):
                line.append(tile[y][x])
            res.append(''.join(line))
        if mod:
            self.tile = res
        return res

    def make_rotations(self):
        res = []
        t = self.tile
        for i in range(4):
            t = self.rotate_tile(t)
            res.append(t)
        t = self.flip_tile(t)
        for i in range(4):
            t = self.rotate_tile(t)
            res.append(t)
        return res

    def flip_tile(self, tile):
        return tile[-1::-1]

    def _get_edges(self, tile=None):
        tile = tile or self.tile
        # Edges are stored left-> right and top->down for easier matching
        left = ""
        right = ""
        for s in tile:
            left += s[0]
            right += s[-1]

        return [tile[0], right, tile[-1], left] # North, East, South, West

    def get_all_edges(self):
        res = []
        for r in self.rotations:
            res.append(self._get_edges(r))
        return res

    def match(self, other):
        return set(self.tiles) == set(other.tiles)

    def findmatches(self, arr):
        res = set()
        for t in [_ for _ in arr if _ != self]:
            if len(t.unique_edges & self.unique_edges ) > 0:
                res.add(t)
        self.neighbors = list(res)

    def count(self):
        return len([_ for _ in "".join(self.tile) if _ == "#"])

tiles = {int(_[0][5:5+4]):Tile(_) for _ in data}

for t in tiles.values():
    t.findmatches(tiles.values())


def find_connected(n):
    return list(set([t for t in tiles.values() if len(t.neighbors) == n]))


def print_all_tiles(alltiles):
    w = int(math.sqrt(len(tiles)))
    for y in range(0, -w, -1):
        for x in range(0, w):
            print(f"{alltiles[(x, y)].number} [{alltiles[(x, y)].rotation}]", end=' ')
        print()
    print("===")


def star1():
    corners = find_connected(2)
    r = 1
    for t in corners:
        r *= int(t.number)
    return r


def rotate_in_place(alltiles):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    w = int(math.sqrt(len(tiles)))
    for y in range(0, -w, -1):
        # Fix first tile in row
        if y < 0:
            c = alltiles[(0,y+1)]
            this = alltiles[(0,y)]
            for i, rotation in enumerate(this.all_edges):
                if c.all_edges[c.rotation][SOUTH] == rotation[NORTH]:
                    this.rotation = i
                    break

        # Traverse eastbound
        for x in range(1, w):
            c = alltiles[(x-1,y)]
            this = alltiles[(x,y)]
            for i, rotation in enumerate(this.all_edges):
                if c.all_edges[c.rotation][EAST] == rotation[WEST]:
                    this.rotation = i
                    break


def fix_upper_left(alltiles):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    c0 = alltiles[(0, 0)]
    cr = alltiles[(1, 0)]
    cd = alltiles[(0, -1)]

    for i, r in enumerate(c0.all_edges):
        for rri, rr in enumerate(cr.all_edges):
            if r[EAST] == rr[WEST]:
                for rdi, rd in enumerate(cd.all_edges):
                    if r[SOUTH] == rd[NORTH]:
                        c0.rotation = i
                        return


def place_tiles():
    def moveleft(x, y):
        return x-1, y

    def movedown(x, y):
        return x, y-1

    def moveright(x, y):
        return x+1, y

    def moveup(x, y):
        return x, y+1

    corners = find_connected(2)
    edges = find_connected(3)
    inner = find_connected(4)

    moves = [moveright, movedown, moveleft, moveup]
    alltiles = {}
    x, y = 0, 0

    c = corners[0]
    consumed = [c]
    alltiles[(x, y)] = c

    # Find corners and edges
    for move in moves:
        while any([_ for _ in c.neighbors if _ in edges and _ not in consumed]):
            c = [_ for _ in c.neighbors if _ in edges and _ not in consumed][0]
            x, y = move(x, y)
            consumed.append(c)
            alltiles[(x, y)] = c

        next_corner = [_ for _ in c.neighbors if _ in corners and _ not in consumed]
        if any(next_corner):
            c = [_ for _ in next_corner][0]
            x, y = move(x, y)
            consumed.append(c)
            alltiles[(x, y)] = c

    # Fill the inner area
    w = int(math.sqrt(len(tiles)))

    while len(consumed) < w * w:
        for y in range(-1, -w+1, -1):
            for x in range(1, w):
                nleft = alltiles.get((x-1, y), None)
                nright = alltiles.get((x+1, y), None)
                ntop = alltiles.get((x, y+1), None)
                nbottom = alltiles.get((x, y-1), None)
                neighbors = [_ for _ in [nleft, nright, ntop, nbottom] if _ is not None]

                potential = []
                for c in [_ for _ in inner if _ not in consumed]:
                    if all([_ in c.neighbors for _ in neighbors]):
                        potential.append(c)
                        alltiles[(x, y)] = c
                        consumed.append(c)

    fix_upper_left(alltiles)
    rotate_in_place(alltiles)
    return alltiles


def print_map(alltiles):
    w = int(math.sqrt(len(tiles)))
    h = len(alltiles[(0, 0)].tile[0])

    for y in range(0, -w, -1):
        for r in range(h):
                for x in range(w):
                    t = alltiles[(x,y)]
                    print(f"{t.rotations[t.rotation][r]}  ", end = "")
                print()
        print()


def combine_map(alltiles):
    w = int(math.sqrt(len(tiles)))
    h = len(alltiles[(0, 0)].tile[0])
    allmap = ["Tile GLOBALMAP:"]

    for y in range(0, -w, -1):
        for rows in range(1, h-1):
            row = []
            for x in range(w):
                t = alltiles[(x,y)]
                row.append(t.rotations[t.rotation][rows][1:-1])

            allmap.append("".join(row))

    return Tile(allmap)


def count_monsters(gmap):
    monster = [
        "Tile Monster:",
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]

    m = Tile(monster)
    m_size = m.count()

    mw = len(m.tile[0])
    mh = len(m.tile)
    max_m = 0
    for r in gmap.rotations:
        m_count = 0
        for y in range(0, len(r) - mh):
            for x in range(0, len(r[y]) - mw):
                # Check monster pattern on each starting point.
                m_hit = 0
                for my in range(mh):
                    for mx in range(mw):
                        if m.tile[my][mx] == "#" and r[y+my][x+mx] == "#":
                            m_hit += 1

                if m_hit == m_size:
                    m_count += 1

        max_m = max([max_m, m_count])
    return max_m, m_size


@timeit
def star2():
    laid_out_grid = place_tiles()
    gmap = combine_map(laid_out_grid)
    monsters, monstersize = count_monsters(gmap)
    return gmap.count() - monsters * monstersize


print(f"* {star1()}")
print(f"** {star2()}")
