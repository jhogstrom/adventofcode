import logging
from collections import defaultdict

from reader import get_data, set_logging, timeit

runtest = False
stardate = "20"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def find_char(char, data):
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == char:
                return x, y
    raise ValueError(f"Could not find {char}")


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def trace_track(start, end, data):
    track = {}
    p = start
    track[p] = 0
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while p != end:
        for _ in neighbors:
            n = add(p, _)
            if (n not in track and data[n[1]][n[0]] == ".") or n == end:
                track[n] = track[p] + 1
                p = n
                break
    return track


@timeit
def star1(data):
    logging.debug("running star 1")
    start = find_char("S", data)
    end = find_char("E", data)

    track = trace_track(start, end, data)
    jump_targets = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    shortcuts = defaultdict(int)
    target_gain = 2 if runtest else 100
    jump_length = 2
    for p in track:
        for _ in jump_targets:
            n = add(p, _)
            if track.get(n, track[p]) >= track[p] + target_gain + jump_length:
                shortcuts[track[n] - track[p] - jump_length] += 1
    print(sum(shortcuts.values()))


def get_jump_targets(n: int):
    result = set()
    for y in range(-n - 1, n + 1):
        for x in range(-(n - abs(y)) - 1, n - abs(y) + 1):
            if abs(x) + abs(y) <= n:
                result.add((x, y))
    return result


@timeit
def star2(data):
    logging.debug("running star 2")
    start = find_char("S", data)
    end = find_char("E", data)

    track = trace_track(start, end, data)
    jump_length = 20
    jump_targets = get_jump_targets(jump_length)
    target_gain = 50 if runtest else 100
    shortcuts = defaultdict(int)
    for p in track:
        for _ in jump_targets:
            n = add(p, _)
            dist = abs(_[0]) + abs(_[1])
            if track.get(n, track[p]) >= track[p] + target_gain + dist:
                shortcuts[track[n] - track[p] - dist] += 1

    print("Count:", sum(shortcuts.values()))


star1(data)
star2(data2)
