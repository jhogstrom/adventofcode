import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "05"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def parse_data(data):
    empty = False
    ranges = []
    ids = []
    for line in data:
        if line == "":
            empty = True
            continue
        if empty:
            ids.append(int(line))
        else:
            a, b = line.split("-")
            ranges.append((int(a), int(b)))
    return ranges, ids


@timeit
def star1(data):
    logging.debug("running star 1")
    ranges, ids = parse_data(data)

    fresh = set()
    for id in ids:
        for a, b in ranges:
            if a <= id <= b:
                fresh.add(id)
                logging.debug(f"star 1: {id} is in range {a}-{b}")
                continue
    logging.info(f"star 1: {len(fresh)}")


@timeit
def star2(data):
    logging.debug("running star 2")
    ranges, _ = parse_data(data)
    print(len(ranges))

    overlap = True
    merged = []
    while overlap:
        overlap = False
        merged = []
        while ranges:
            r_min, r_max = ranges.pop(0)
            for i, (c_min, c_max) in enumerate(ranges):
                if not (r_max < c_min or r_min > c_max):
                    logging.debug(f"Merging {r_min}-{r_max} with {c_min}-{c_max}")
                    r_min = min(r_min, c_min)
                    r_max = max(r_max, c_max)
                    overlap = True
                    ranges.pop(i)
                    break
            merged.append((r_min, r_max))
        ranges = merged[:]

    c_min = 0
    for r_min, r_max in ranges:
        c_min += r_max - r_min + 1
    logging.info(f"star 2: {c_min}")


star1(data)
star2(data2)
