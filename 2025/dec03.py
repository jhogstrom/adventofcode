import logging
from typing import List  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "03"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_max_joltage2(MAX: int, adapters: List[str]) -> int:
    result = ""
    org = "".join(adapters)
    while len(result) < MAX:
        if len(result) + len(adapters) == MAX:
            result += "".join(adapters)
            break
        batch = adapters[: len(adapters) - MAX + len(result) + 1]
        largest = max(batch)
        result += largest
        p = adapters.index(largest)
        adapters = adapters[p + 1 :]  # noqa E203
    logging.debug(f"get_max_joltage2:\n\t{org} -> \n\t{result} ({len(result)})")
    return int(result)


def total_joltage(MAX: int, data) -> int:
    result = 0
    for c, line in enumerate(data):
        logging.debug(f"line {c}/{len(data)}")
        result += get_max_joltage2(MAX, list(line))
    return result


@timeit
def star1(data):
    logging.debug("running star 1")
    result = total_joltage(2, data)
    logging.info(f"star 1: {result}")


@timeit
def star2(data):
    logging.debug("running star 2")
    result = total_joltage(12, data)
    logging.info(f"star 2: {result}")


star1(data)
star2(data2)
