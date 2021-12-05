import os
from timer import timeit

stardate = 4
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

class Board():
    def __init__(self, b):
        self.won = False
        self.rows = []
        self.played = []
        for row in b:
            self.rows.append([int(_) for _ in row.split()])
            self.played.append([False for _ in row.split()])

    def play(self, n):
        for i, r in enumerate(self.rows):
            if n in r:
                p = r.index(n)
                self.played[i][p] = True

    def bingo(self):
        if self.won:
            return False
        for r in self.played:
            if all(r):
                self.won = True
                return True

        for col in range(5):
            colbingo = True
            for row in self.played:
                colbingo &= row[col]
            if colbingo:
                self.won = True
                return True

        return False

    def rowstr(self, r):
        res = []
        for i, n in enumerate(self.rows[r]):
            if self.played[r][i]:
                res.append(f"[{n}]")
            else:
                res.append(f"{n}")
        return str(" ".join([f"{_:>4}" for _ in res]))

    def calc(self, n):
        res = 0
        for r in range(5):
            for c in range(5):
                if not self.played[r][c]:
                    res += self.rows[r][c]
        # print(res)
        return res * n


    def __str__(self):
        # return "\n".join([str(_) for _ in self.rows])
        return "\n".join([self.rowstr(_) for _ in range(len(self.rows))])


def play(n, boards):
    for b in boards:
        b.play(n)
        if b.bingo():
            print("bingo", b.calc(n))
            # print(str(b))

def star1(data):
    randnums = [int(_) for _ in data[0].split(",")]
    # randnums = [22, 8, 21, 6, 1]
    boards = []
    data = data[2:]
    b = []
    for s in data:
        b.append(s)
        if len(b) == 6:
            boards.append(Board(b[:-1]))
            # print("appending", b[:-1])
            b = []
    boards.append(Board(b))

    for n in randnums:
        # print("drawing", n)
        play(n, boards)

    # for b in boards:
    #     print(str(b))
    #     print()


def star2():
    ...

star1(data)
star2()