from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "4"
set_logging(runtest)
data = get_data(stardate, runtest)
data2 = data[:]


def get_wincount(card) -> int:
    winners, numbers = card.split(":")[1].split("|")
    winners = [_ for _ in winners.split()]
    numbers = [_ for _ in numbers.split()]
    return len([_ for _ in numbers if _ in winners])

@timeit
def star1(data):
    res = 0
    for _ in data:
        # winners, numbers = _.split(":")[1].split("|")
        count = get_wincount(_)
        value = 2 ** (count-1) if count else 0
        res += value
        # logging.debug(f"{winners}  {numbers}  => {count} = {value} res: {res}")

    print(res)


@timeit
def star2(data):
    cardpile = defaultdict(int)
    for i, _ in enumerate(data):
        cardpile[i] += 1
        wincount = get_wincount(_)
        for j in range(i+1, i+wincount+1):
            cardpile[j] += cardpile[i]
        #     logging.debug(f"\tCard {j} => {cardpile[j]}")
        # logging.debug(f"Card {i} => {wincount} {cardpile}")

    print(sum(cardpile.values()))


star1(data)
star2(data2)
