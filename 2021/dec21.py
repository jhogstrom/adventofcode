import os
from typing import List
from timer import timeit
from collections import defaultdict
import itertools

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

    dice = Dice()
    c = 0
    while not any (_.haswon for _ in players):
        for p in players:
            p.play(dice)
            if p.haswon:
                break
        c += 1

    loser = [_ for _ in players if not _.haswon][0]
    print(loser.points * dice.rollcount)


class BoardState():
    def __init__(self, positions) -> None:
        self.count = 0
        self.positions = positions
        self.scores = [0, 0]
        self.next_turn = 0

    def after_move(self, m):
        res = BoardState(self.positions)
        res.positions[self.next_turn] += m
        res.positions[self.next_turn] %= 10
        res.scores[self.next_turn] += res.positions[self.next_turn]
        res.next_turn = (self.next_turn + 1) % 2
        return res

    def __eq__(self, __o: object) -> bool:
        return self.positions == __o.positions \
            and self.scores == __o.scores \
            and self.next_turn == __o.next_turn

    # def __hash__(self) -> int:
    #     return hash(self.positions, self.positions[1],
    #         self.scores[0], self.scores[1] * 7 \
    #         + self.scores * 11


    def roll_die(self):
        res = set([self])
        for _ in range(3):
            newboards = []
            for b in res:
                nextround = []
                for d in range(1, 4):
                    nextround.append(b.after_move(d))
                newboards.extend(nextround)
            res = newboards

        return res


@timeit
def star2(data):
    startpositions = [int(_.split()[-1]) for _ in data]

    dice = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    dice_results = itertools.product(*dice)
    dicerolls = defaultdict(int)
    for _ in dice_results:
        dicerolls[sum(_)] += 1

    P1POS, P2POS, P1SCORE, P2SCORE = 0, 1, 2, 3
    PLAYER1, PLAYER2 = 0, 1

    pos = { PLAYER1: P1POS, PLAYER2: P2POS}
    score = { PLAYER1: P1SCORE, PLAYER2: P2SCORE}
    wins = {PLAYER1: 0, PLAYER2: 0}
    boards = {(startpositions[0] % 10, startpositions[1] % 10, 0, 0): 1}

    MAXSCORE, rounds, player = 21, 0, 0
    while boards:
        newboards = defaultdict(int)
        for steps, count in dicerolls.items():
            # print(f"Rolling {steps} - {count} times")
            for board in boards.keys():
                # Convert tuple to list allowing modification of items
                newworld = list(board)
                # Move steaps forward and mod by 10
                newworld[pos[player]] = (board[pos[player]] + steps) % 10
                # Hand out points - pos0 gives 10 points due to the mod above
                newworld[score[player]] += newworld[pos[player]] or 10
                # How many worlds have been created?
                worldcount = boards[board] * count
                # If this world made `player` win, count the wins
                if newworld[score[player]] >= MAXSCORE:
                    wins[player] += worldcount
                # Else we're in for another round
                else:
                    newboards[tuple(newworld)] += worldcount
            # Next player to play
        player = (player + 1) % 2
        rounds += 1
        boards = newboards.copy()

        games_in_progress = sum(list(boards.values()))
        completed_games = sum(list(wins.values()))
        print(f"Rounds: {rounds:>3} Games: {completed_games:>15} / {games_in_progress:>15} Worlds: {len(boards):>10}")


    print(f">Player1: {wins[PLAYER1]:>15} Player2: {wins[PLAYER2]:>15}")
    # Expected results for test data
    # print(f"!Player1: {444356092776315:>15} Player2: {341960390180808:>15}")

star1(data)
star2(data)
