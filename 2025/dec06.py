import logging
from collections import defaultdict, deque
from typing import List, Tuple  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "06"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest, dostrip=False)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    columns = defaultdict(deque)
    for line in data:
        parts = line.split()
        for c, part in enumerate(parts):
            columns[c].append(part)

    for c, values in columns.items():
        logging.debug(f"Column {c}: {values}")

    result = 0
    for c, values in columns.items():
        op = values.pop()
        logging.debug(f"Column {c} operation: {op}")
        res = 0 if op == "+" else 1
        while values:
            a = int(values.popleft())
            if op == "+":
                res += a
            elif op == "*":
                res *= a
            else:
                raise ValueError(f"Unknown operation {op}")
            logging.debug(f"{op} {a} = {res}")
            # values.appendleft(str(res))
        result += res
        logging.debug(f"Column {c} result: {res}")
    logging.info(f"star 1: {result}")


def get_column(data, maxlen: List[int], col: int) -> List[str]:
    start = sum(maxlen[:col]) + col
    end = start + maxlen[col]
    # logging.debug(f"Column {col} start: {start}, end: {end}")
    # for line in data:
    #     logging.debug(f"Line: >{line}< -> >{line[start:end]}<")
    return [line[start:end] for line in data]


def read_numbers(column: List[str], maxlen) -> Tuple[str, List[int]]:
    op = column[-1].strip()
    numbers = [""] * (len(column) - 1)
    for n, num in enumerate(column[:-1]):
        if len(num) < maxlen:
            num = num.ljust(maxlen)
        # logging.debug(f"Reading number {n}: >{num}<")
        for i in range(maxlen):
            numbers[i] += num[i]
            # logging.debug(f"Reading char {i} -> {num[i]} -> >{numbers[i]}<")

    # logging.debug(f"Operation: >{op}<, numbers: {numbers}")
    return op, [int(x) for x in numbers if x]


@timeit
def star2(data):
    logging.debug("running star 2")
    columns = defaultdict(deque)
    maxlen: List[int] = []
    for line in data:
        parts = line.split()
        maxlen = maxlen or [0] * len(parts)
        for c, part in enumerate(parts):
            columns[c].append(part)
            if maxlen[c] < len(part):
                maxlen[c] = len(part)

    result = 0
    for c in range(len(columns)):
        logging.debug(f"Processing column {c}")

        column = get_column(data, maxlen, c)
        # logging.debug(f"Column {c} data: {column}")
        op, numbers = read_numbers(column, maxlen[c])
        # logging.debug(f"Column {c}: {op}, {numbers}")
        r = 0 if op == "+" else 1
        for n in numbers:
            if op == "+":
                r += n
                # logging.debug(f"{r - n} + {n} = {r}")
            elif op == "*":
                r *= n
                # logging.debug(f"{r // n} * {n} = {r}")
        result += r
        # logging.debug(f"Column {c} result: {r}")
    logging.info(f"star 2: {result}")


star1(data)
star2(data2)
