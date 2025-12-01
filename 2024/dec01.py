import logging
import sys
from pathlib import Path

# Add repo root to path to enable helpers import
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.reader import get_data, set_logging, timeit  # noqa E402

runtest = False
stardate = "01"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    l1 = []
    l2 = []
    for s in data:
        l1.append(int(s.split()[0]))
        l2.append(int(s.split()[1]))

    l1 = sorted(l1)
    l2 = sorted(l2)
    result = 0
    for i, v in enumerate(l1):
        result += abs(v - l2[i])
    print(result)


@timeit
def star2(data):
    logging.debug("running star 2")
    l1 = []
    l2 = []
    for s in data:
        l1.append(int(s.split()[0]))
        l2.append(int(s.split()[1]))
    result = 0
    for i in l1:
        result += i * l2.count(i)
    print(result)


star1(data)
star2(data2)
