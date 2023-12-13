from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "13"
year = "2023"

set_logging(runtest)
testnum = "2"
if not runtest:
    testnum = ""
data = get_data(stardate, year, runtest, testnum)

def is_matching(left, right):
    shortest = min(len(left), len(right))
    for i in range(shortest):
        if left[i] != right[i]:
            return False
    return True

def find_match_points(_, possibilities, smudge_pos=None):
    res = set()
    for r in possibilities:
        left = _[:r][::-1]
        right = _[r:]
        ismatch = is_matching(left, right)
        if ismatch and smudge_pos is not None:
            if (len(left) < len(right) and smudge_pos >= 2 * len(left)) or \
                (len(left) > len(right) and smudge_pos <= len(_) - 2 * len(right)):
                ismatch = False
        if ismatch:
            # print(f"Match at {r} between {left} and {right}")
            res.add(r)
    return res


def find_vertical_reflection(pattern, x=None):
    # logging.debug("Finding vertical reflection")
    possibilities = set(range(1, len(pattern[0])))

    for _ in pattern:
        possibilities = possibilities.intersection(find_match_points(_, possibilities, x))
        if not possibilities:
            return 0

    return list(possibilities)[0]


def find_horizontal_reflection(pattern, y=None):
    # logging.debug("Finding horizontal reflection")
    possibilities = set(range(1, len(pattern)))

    for x in range(len(pattern[0])):
        _ = "".join([_[x] for _ in pattern])
        possibilities = possibilities.intersection(find_match_points(_, possibilities, y))
        if not possibilities:
            return 0

    return list(possibilities)[0]


def check_pattern(pattern, x=None, y=None):
    res = 100 * find_horizontal_reflection(pattern, y)
    if not res:
        res = find_vertical_reflection(pattern, x)
    return res


@timeit
def star1(data):
    logging.debug("running star 1")
    pattern = []
    res = 0
    for _ in data:
        pattern.append(_)
        if not _:
            res += check_pattern(pattern[:-1])
            pattern = []

    res += check_pattern(pattern)
    print(res)


flip = {".": "#", "#": "."}


def modify_pattern(pattern, x, y):
    res = pattern[:]
    res[y] = res[y][:x] + flip[res[y][x]] + res[y][x + 1:]
    return res


def print_pattern(p, title):
    print(title)
    for i, _ in enumerate(p):
        print(f"{i:2} {_}")
    print("===")


def check_smudged_pattern(pattern):
    # print_pattern(pattern, "Original pattern")
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            res = check_pattern(modify_pattern(pattern, x, y), x, y)
            if res:
                # print_pattern(
                #   modify_pattern(pattern, x, y),
                #   f"Original pattern\nScore: {res} at {x} {y}")
                return res
    raise ValueError("No reflection found")


@timeit
def star2(data):
    logging.debug("running star 2")
    pattern = []
    res = 0
    for _ in data:
        pattern.append(_)
        if not _:
            res += check_smudged_pattern(pattern[:-1])
            pattern = []

    res += check_smudged_pattern(pattern)
    print(res)


star1(data)
star2(data)
