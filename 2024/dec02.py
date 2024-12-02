import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "02"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    result = 0
    for s in data:
        values = [int(_) for _ in s.split()]
        if is_safe(values):
            result += 1
    print(result)


def is_safe(values):
    diffs = [(values[i] - values[i - 1]) for i in range(1, len(values))]
    return all([d in [1, 2, 3] for d in diffs]) or all(
        [d in [-1, -2, -3] for d in diffs]
    )


@timeit
def star2(data):
    result = 0
    for s in data:
        values = [int(_) for _ in s.split()]
        for i in range(len(values)):
            v2 = values[:i] + values[i + 1 :]  # noqa
            if is_safe(v2):
                result += 1
                break
    print(result)


star1(data)
star2(data2)
