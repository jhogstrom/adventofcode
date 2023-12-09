import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "9"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def get_differences(numbers):
    history = [numbers]
    while not all([_ == 0 for _ in history[-1]]):
        new = []
        for i in range(len(history[-1]) - 1):
            new.append(history[-1][i + 1] - history[-1][i])
        history.append(new)
    return history


def extrapolate_forward(numbers):
    history = get_differences(numbers)[::-1]

    for i in range(len(history)-1):
        history[i+1].append(history[i][-1] + history[i+1][-1])
    return history[-1][-1]


def extrapolate_backward(numbers):
    history = get_differences(numbers)[::-1]

    for i in range(len(history)-1):
        history[i+1].insert(0, history[i+1][0] - history[i][0])
    return history[-1][0]


@timeit
def star1(data):
    logging.debug("running star 1")
    res = 0
    for _ in data:
        res += extrapolate_forward([int(_) for _ in _.split()])
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    res = 0
    for _ in data:
        res += extrapolate_backward([int(_) for _ in _.split()])
    print(res)


star1(data)
star2(data2)
