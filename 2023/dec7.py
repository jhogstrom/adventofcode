from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "7"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]

cardvalues_star1 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

cardvalues_star2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

class Hand():
    def __init__(self, cards, bid, valuemap, jokers) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.jokers = jokers
        self.value = self._value()
        self.valuemap = valuemap

    def __repr__(self) -> str:
        return f"{self.bid:3}: {self.cards} - {self.value} - {self.hand_type()}"

    def hand_type(self):
        if self.value == 7:
            return "5 of a kind"
        if self.value == 6:
            return "4 of a kind"
        if self.value == 5:
            return "Full house"
        if self.value == 4:
            return "3 of a kind"
        if self.value == 3:
            return "2 pair"
        if self.value == 2:
            return "1 pair"
        return "High card"

    def _value(self):
        buckets = {}
        for c in self.cards:
            buckets[c] = buckets.get(c, 0) + 1
        if self.jokers:
            jokers = buckets.get("J", 0)
            if jokers > 0:
                buckets["J"] = 0
                m = 0
                mc = None
                for k, v in buckets.items():
                    if v > m:
                        m = v
                        mc = k
                buckets[mc if mc else "J"] += jokers

            # print(f"{self.cards} has {jokers} jokers")
        values = list(buckets.values())
        if 5 in values:
            return 7
        if 4 in values:
            return 6
        if 3 in values and 2 in values:
            return 5
        if 3 in values:
            return 4
        if len(values) == 3:
            return 3
        if 2 in values:
            return 2
        return 1

    def __gt__(self, other):
        if self.value < other.value:
            return False
        if self.value > other.value:
            return True
        for i, c in enumerate(self.cards):
            c = self.valuemap[c]
            if c > self.valuemap[other.cards[i]]:
                return True
            if c < self.valuemap[other.cards[i]]:
                return False



@timeit
def star1(data):
    logging.debug("running star 1")
    hands = sorted([Hand(*_.split(), cardvalues_star1, False) for _ in data])
    res = 0
    for i, h in enumerate(hands, 1):
        # print(i, h)
        res += i * h.bid
    print(res)



@timeit
def star2(data):
    logging.debug("running star 2")
    hands = sorted([Hand(*_.split(), cardvalues_star2, True) for _ in data])
    res = 0
    for i, h in enumerate(hands, 1):
        # print(i, h)
        res += i * h.bid
    print(res)


star1(data)
star2(data2)
