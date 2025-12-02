import logging
import re  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "02"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def match_range(r, pattern):
    start, end = map(int, r.split("-"))
    s = 0
    for id in range(start, end + 1):
        if pattern.findall(str(id)):
            s += id
    return s


def check_data(data, regexp: str):
    pattern = re.compile(regexp)
    s = 0
    for line in data:
        for r in line.split(","):
            s += match_range(r, pattern)
    return s


@timeit
def star1(data):
    logging.debug("running star 1")
    s = check_data(data, r"^(\d+)(\1)$")
    logging.info(f"star 1: {s}")


@timeit
def star2(data):
    logging.debug("running star 2")
    s = check_data(data, r"^(\d+)(\1{1,})$")
    logging.info(f"star 2: {s}")


star1(data)
star2(data2)
