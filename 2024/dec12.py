import logging
from collections import defaultdict, deque
from typing import List, Set, Tuple  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "12"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_regions(plots: List[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    regions = []
    while plots:
        queue = deque([plots[0]])
        r = set()
        while queue:
            x, y = queue.pop()
            if (x, y) in plots:
                r.add((x, y))
                plots.remove((x, y))
                queue.append((x + 1, y))
                queue.append((x - 1, y))
                queue.append((x, y + 1))
                queue.append((x, y - 1))
        regions.append(r)
    return regions


def calculate_perimeter_and_area(region: Set[Tuple[int, int]]) -> Tuple[int, int]:
    perimeter = 0
    for x, y in region:
        n, e, w, s = (x, y - 1), (x + 1, y), (x - 1, y), (x, y + 1)
        perimeter += 4 - sum(1 for p in [n, e, w, s] if p in region)
    return perimeter * len(region)


@timeit
def star1(data):
    logging.debug("running star 1")
    plots = defaultdict(list)
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            plots[c].append((x, y))

    regions = []
    for crop in plots.values():
        regions.extend(get_regions(crop))
    print(len(regions))

    price = sum(calculate_perimeter_and_area(r) for r in regions)
    print(price)


def count_edges(numlist: List[int]) -> int:
    if not numlist:
        return 0
    edges = 1
    for i in range(1, len(numlist)):
        if numlist[i] - numlist[i - 1] > 1:
            edges += 1
    return edges


def print_region(
    region: Set[Tuple[int, int]], c_min: Tuple[int, int], c_max: Tuple[int, int]
) -> None:
    for y in range(c_min[1], c_max[1] + 1):
        for x in range(c_min[0], c_max[0] + 1):
            if (x, y) in region:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()
    input()


def calculate_edges_and_area(region: Set[Tuple[int, int]]) -> Tuple[int, int]:
    c_min = (min(x for x, _ in region), min(y for _, y in region))
    c_max = (max(x for x, _ in region), max(y for _, y in region))

    edges = 0
    for y in range(c_min[1], c_max[1] + 1):
        upper = []
        lower = []
        for x in range(c_min[0], c_max[0] + 1):
            if (x, y) not in region:
                continue
            if (x, y - 1) not in region:
                upper.append(x)
            if (x, y + 1) not in region:
                lower.append(x)
        edges += count_edges(sorted(upper))
        edges += count_edges(sorted(lower))
    for x in range(c_min[0], c_max[0] + 1):
        left = []
        right = []
        for y in range(c_min[1], c_max[1] + 1):
            if (x, y) not in region:
                continue
            if (x - 1, y) not in region:
                left.append(y)
            if (x + 1, y) not in region:
                right.append(y)
        edges += count_edges(sorted(left))
        edges += count_edges(sorted(right))

    return edges * len(region)


@timeit
def star2(data):
    logging.debug("running star 2")
    plots = defaultdict(list)
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            plots[c].append((x, y))

    regions = []
    for crop in plots.values():
        regions.extend(get_regions(crop))

    price = sum(calculate_edges_and_area(r) for r in regions)

    print(price)


star1(data)
star2(data2)
