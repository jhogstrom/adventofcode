import logging
import sys
from collections import defaultdict, deque  # noqa E401
from pathlib import Path

# Add repo root to path to enable helpers import
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.reader import get_data, set_logging, timeit  # noqa E402

runtest = True
stardate = "X"
year = "YEAR"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
