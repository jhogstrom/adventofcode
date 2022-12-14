import os

runtest = False
stardate = "12"
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Cell():
    def __init__(self, x: int, y: int, data, parent=None) -> None:
        self.x = x
        self.y = y
        self.data = data
        self.parent = parent
        self._char = None
        self._path = None
        self.direction = None

    def path(self):
        if self._path is None:
            res = [self]
            n = self
            while n.parent is not None:
                n = n.parent
                res.append(n)
            self._path = res
        return self._path

    def neighbors(self):
        res = []
        # left
        if self.x > 0:
            res.append(Cell(self.x-1, self.y, data, self))
        # up
        if self.y > 0:
            res.append(Cell(self.x, self.y-1, data, self))
        # right
        if self.x < len(data[self.y])-1:
            res.append(Cell(self.x+1, self.y, data, self))
        # down
        if self.y < len(data) - 1:
            res.append(Cell(self.x, self.y+1, data, self))
        return res

    @property
    def char(self):
        if self._char is None:
            self._char = data[self.y][self.x]
        return self._char

    @property
    def path_length(self):
        return len(self.path())

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y}): {self.char}"

    def can_visit(self, target) -> bool:
        c = target.char if target.char != "E" else "z"
        if c == "S":
            return False
        if self.char == "S":
            return True
        return ord(self.char) + 1 >= ord(c)


# @timeit
def find_position(target: str):
    for r, s in enumerate(data):
        try:
            return Cell(s.index(target), r, data)
        except ValueError:
            pass


def print_path(p):
    for i, n in enumerate(p[::-1]):
        print(f"{i:>3} {n}")


def solve(start: Cell):  # NOSONAR
    goal = find_position("E")

    to_visit = [start]
    visited = []
    while len(to_visit) > 0:
        curr = to_visit[0]
        index = 0
        for ix, n in enumerate(to_visit):
            if n.path_length < curr.path_length:
                curr = n
                index = ix

        to_visit.pop(index)
        if curr in visited:
            continue
        visited.append(curr)

        if curr == goal:
            return curr.path()

        for n in curr.neighbors():
            if n not in visited and curr.can_visit(n):
                to_visit.append(n)

    return []


def star1():
    p = solve(find_position("S"))
    return len(p)-1


def star2():  # NOSONAR
    seen_starts = []
    min_steps = 999999
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == "a":
                start = Cell(x, y, data)
                if start in seen_starts:
                    continue
                print(f"Solving for {start}", end="\r")
                p = solve(start)
                length = 0
                for n in p:
                    if n.char == "a":
                        seen_starts.append(n)
                        min_steps = min([min_steps, length])
                        print(min_steps, len(seen_starts), end="\r")
                    length += 1
    return min_steps


# print("star1:", star1())
print("star2:", star2())
