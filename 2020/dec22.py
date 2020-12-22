import helpers
from timing import timeit

extra = "_demo"
extra = ""
data = helpers.get_data(__file__, extra=extra)

player1, player2 = helpers.get_records(data)

player1 = [int(_) for _ in player1[1:]]
player2 = [int(_) for _ in player2[1:]]


def star1(player1, player2):
    while player1 and player2:
        deal = [player1.pop(0), player2.pop(0)]
        if deal[0] > deal[1]:
            player1 += deal
        else:
            player2 += deal[-1::-1]

    winner = player1 or player2
    r = 0
    for i, v in enumerate(winner[-1::-1]):
        r += ((i+1) * v)
    return r


def playgame(p1, p2, level=0):
    # print(f"Level {level}")
    # print(f"New game {level}:\n\t{p1}\n\t{p2}")
    p1_hands, p2_hands, c = [], [], 1
    while p1 and p2:
        # print(f"P1 deck: {p1}\nP2 deck: {p2}")

        if p1 in p1_hands or p2 in p2_hands:
            # print(f"preexisting hand! {p1_hands} -- {p2_hands}")
            return 0, p1, p2

        p1_hands.append(p1.copy())
        p2_hands.append(p2.copy())

        c1, c2 = p1.pop(0), p2.pop(0)
        # print(f"Player1 plays: {c1}\nPlayer2 plays: {c2}")

        if len(p1) >= c1 and len(p2) >= c2:
            winner, x, x = playgame(p1[:c1], p2[:c2], level+1)
        else:
            if c1 > c2:
                winner = 0
            else:
                winner = 1

        # print(f"Player {winner + 1} wins round {c}\n")
        if winner == 0:
            p1 += [c1, c2]
        else:
            p2 += [c2, c1]
        c += 1


    return int(not p1), p1, p2
    if p1:
        return 0, p1, p2
    else:
        return 1, p1, p2



@timeit
def star2(p1, p2):
    winner, p1, p2 = playgame(p1, p2)
    winner = p1 or p2
    r = 0
    for i, v in enumerate(winner[-1::-1]):
        r += ((i+1) * v)
    return r


print(f"* {star1(player1.copy(), player2.copy())}")
print(f"* {star2(player1.copy(), player2.copy())}")



