import os
from typing import List
from timer import timeit
from collections import defaultdict, deque

stardate = 21
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Dice():
    def __init__(self) -> None:
        self.val = 1
        self.rollcount = 0

    def roll(self):
        res = self.val
        self.val += 1
        self.val = self.val % 100
        self.rollcount += 1
        return res

class Player():
    def __init__(self, name, startingpoints: int) -> None:
        self.name = name
        self.points = 0
        self.boardpos = startingpoints - 1

    def __str__(self) -> str:
        return f"{self.name}: {self.points}"

    def play(self, dice: Dice):
        moves = []
        for _ in range(3):
            moves.append(dice.roll())

        self.boardpos += sum(moves)
        self.boardpos %= 10
        self.points += self.boardpos + 1

        # print(f"{self.name} rolls {moves} " \
        #        f"and moves to space {self.boardpos + 1} " \
        #        f"for a total score of {self.points}")



    @property
    def haswon(self):
        return self.points >= 1000

@timeit
def star1(data):
    players: List[Player] = []
    for i, p in enumerate(data):
        players.append(Player(i, int(p.split()[-1])))
    # print(points)

    dice = Dice()
    c = 0
    while not any (_.haswon for _ in players):
        for p in players:
            p.play(dice)
            if p.haswon:
                break
        c += 1
        # print(f"{players[0]} - {players[1]}")
        # print()
        # if c == 10:
        #     exit()

    loser = [_ for _ in players if not _.haswon][0]
    print(loser.points * dice.rollcount)





@timeit
def star2(data):
    rounds = 2 * 3 ** 1
    print(rounds)
    s = 0
    for i in range(10, 1):
        s += 1
        print(i, s)

data2 = data[:]
star1(data)
star2(data2)