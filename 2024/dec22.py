import logging
from typing import List  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "22"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def make_secret(n, c) -> int:
    for _ in range(c):
        n = ((n << 6) ^ n) % 16777216
        n = ((n >> 5) ^ n) % 16777216
        n = ((n << 11) ^ n) % 16777216
    return n


def get_prices(n, c) -> List[int]:
    result = [n % 10]
    for _ in range(c):
        n = ((n << 6) ^ n) % 16777216
        n = ((n >> 5) ^ n) % 16777216
        n = ((n << 11) ^ n) % 16777216
        result.append(n % 10)
    return result


@timeit
def star1(data):
    logging.debug("running star 1")
    initial_numbers = [int(_) for _ in data]
    result = 0
    for n in initial_numbers:
        r = make_secret(n, 2000)
        result += r
    print(result)


@timeit
def star2(data):
    logging.debug("running star 2")
    initial_numbers = [int(_) for _ in data]

    print("Generating prices and deltas...", end="", flush=True)
    prices = []
    deltas = []
    for n in initial_numbers:
        price = get_prices(n, 2000)
        prices.append(price)
        deltas.append([price[i] - price[i - 1] for i in range(1, len(price))])
    print(sum(len(_) for _ in deltas))

    print("Generating sequences...", end="", flush=True)
    all_sequences = []
    for r in range(len(prices)):
        sequences = {}
        delta = deltas[r]
        price = prices[r]
        for i in range(4, len(delta) + 1):
            seq = tuple(delta[i - 4 : i])  # noqa E203
            if seq not in sequences:
                sequences[seq] = price[i]
        all_sequences.append(sequences)
    print(sum(len(_) for _ in all_sequences))

    print("Generating set of sequences...", end="", flush=True)
    all_seqs = set()
    for _ in all_sequences:
        all_seqs.update(_.keys())
    print(len(all_seqs))

    print("Calculating max total...")
    max_total = 0
    for seq in all_seqs:
        total = 0
        for round in range(len(all_sequences)):
            total += all_sequences[round].get(seq, 0)
        if total > max_total:
            max_total = total
    print(max_total)


star1(data)
star2(data2)
