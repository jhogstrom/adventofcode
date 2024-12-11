import logging
from collections import defaultdict

from reader import get_data, set_logging, timeit

runtest = False
stardate = "11"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    stones = [int(_) for _ in data.split(" ")]
    for _ in range(25):
        head = 0
        while head < len(stones):
            stone = stones[head]
            if stone == 0:
                stones[head] = 1
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                stones[head] = int(s[len(s) // 2 :])  # noqa E203
                stones.insert(head, int(s[: len(s) // 2]))
                head += 1
            else:
                stones[head] = stone * 2024
            head += 1
        # print(_, len(stones))
    print(len(stones))


@timeit
def star2(data):
    logging.debug("running star 2")
    stones = {int(_): 1 for _ in data.split(" ")}
    # print(stones)
    for _ in range(75):
        next_round = defaultdict(int)
        for s, v in stones.items():
            if s == 0:
                next_round[1] += v
            elif len(str(s)) % 2 == 0:
                as_str = str(s)
                next_round[int(as_str[len(as_str) // 2 :])] += v  # noqa E203
                next_round[int(as_str[: len(as_str) // 2])] += v
            else:
                next_round[s * 2024] += v
        stones = next_round.copy()

    print(sum(stones.values()))


star1(data[0])
star2(data2[0])
