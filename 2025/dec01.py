import logging
import sys
from pathlib import Path

# Add repo root to path to enable helpers import
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.reader import get_data, set_logging, timeit  # noqa E402

runtest = False
stardate = "01"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    current = 50
    pwd = 0
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        if direction == "R":
            current = (current + amount) % 100
        elif direction == "L":
            current = (current - amount) % 100
        else:
            raise ValueError(f"Unknown direction {direction}")
        logging.debug(f"{line} -> [{direction} {amount}] -> [{current}]")
        if current == 0:
            pwd += 1
    logging.info(f"star 1: {pwd}")


@timeit
def star2(data):
    logging.debug("running star 2")
    current = 50
    pwd = 0
    logging.debug(f"Starting at {current}")
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        d = -1 if direction == "L" else 1
        logging.debug(f"Moving from {current} -> {line}")
        pass0 = 0
        for _ in range(amount):
            current = (current + d) % 100
            if current == 0:
                pass0 += 1
        if pass0:
            logging.debug(f"** Wrapped around {pass0} times")
            pwd += pass0
    logging.info(f"star 2: {pwd}")


star1(data)
star2(data2)
