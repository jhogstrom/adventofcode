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


def play(n, boards, winners):
    for b in boards:
        b.play(n)
        if b.bingo():
            winners.append(b.calc(n))
            # print("bingo", b.calc(n))


def play_boards(randnums, boards, max_wins: int = 0):
    winners = []
    for n in randnums:
        # print("drawing", n)
        play(n, boards, winners)
        if max_wins and len(winners) >= max_wins:
            return winners
    return winners


def parse_data(data):
    randnums = [int(_) for _ in data[0].split(",")]

    boards = []
    board_lines = []
    for s in data[2:]:
        board_lines.append(s)
        if len(board_lines) == 6:
            boards.append(Board(board_lines[:-1]))
            board_lines = []
    boards.append(Board(board_lines))
    return randnums, boards


@timeit
def star1(randnums, boards):
    winners = play_boards(randnums, boards, max_wins=1)
    print(winners[0])


@timeit
def star2(randnums, boards):
    winners = play_boards(randnums, boards)
    print(winners[-1])


randnums, boards = parse_data(data)
star1(randnums, boards)
star2(randnums, boards)