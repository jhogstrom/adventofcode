import os

runtest = False
stardate = "02"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

if not data:
    raise FileNotFoundError(f"No data in {dataname}")


def star1() -> int:
    handvalue = {
        "X": 1,  # rock
        "Y": 2,  # paper
        "Z": 3   # scissors
    }
    wins = {"A": "Y", "B": "Z", "C": "X"}
    draws = {"A": "X", "B": "Y", "C": "Z"}

    score = 0
    for _ in data:
        opponent, me = _.split()
        roundscore = handvalue[me]
        if me == wins[opponent]:
            roundscore += 6
        if me == draws[opponent]:
            roundscore += 3
        score += roundscore
        # print(_, roundscore)
    return score


def star2() -> int:
    # X = I lose
    # Y = draw
    # Z = I win
    handvalue = {"A": 1, "B": 2, "C": 3}
    resultscore = {"X": 0, "Y": 3, "Z": 6}
    myhand = {
        "X": {"A": "C", "B": "A", "C": "B"},
        "Y": {"A": "A", "B": "B", "C": "C"},
        "Z": {"A": "B", "B": "C", "C": "A"}
    }
    score = 0
    for _ in data:
        roundscore = 0
        opponent, result = _.split()
        roundscore = resultscore[result]
        i_play = myhand[result][opponent]
        roundscore += handvalue[i_play]
        score += roundscore
        # print(_, i_play, roundscore)
    return score


print("star1:", star1())
print("star2:", star2())
if runtest:
    print("USING TESTDATA")
