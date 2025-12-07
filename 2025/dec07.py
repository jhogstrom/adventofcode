import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "07"
year = "2025"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    data[0] = data[0].replace("S", "|")
    data = [list(line) for line in data]
    for line in data:
        logging.debug(f"Line: >{line}<")

    splits = 0
    for y, line in enumerate(data[:-1]):
        s = 0
        for x, c in enumerate(line):
            if c == "|":
                if data[y + 1][x] == ".":
                    data[y + 1][x] = "|"
                elif data[y + 1][x] == "^":
                    splits += 1
                    s += 1
                    if x > 0:
                        data[y + 1][x - 1] = "|"
                    if x < len(line) - 1:
                        data[y + 1][x + 1] = "|"
        logging.debug(f"{''.join(line)} -- splits: {s}")
    logging.info(f"star 1: {splits}")


@timeit
def star2(data):
    logging.debug("running star 2")
    worldlines = [[0] * len(data[0]) for _ in range(len(data))]
    worldlines[0][data[0].index("S")] = 1
    data[0] = data[0].replace("S", "|")
    data = [list(line) for line in data]

    for y, line in enumerate(data[:-1]):
        for x, c in enumerate(line):
            if c == "|":
                if data[y + 1][x] in [".", "|"]:
                    data[y + 1][x] = "|"
                    worldlines[y + 1][x] += worldlines[y][x]
                elif data[y + 1][x] == "^":
                    if x > 0:
                        data[y + 1][x - 1] = "|"
                        worldlines[y + 1][x - 1] += worldlines[y][x]
                    if x < len(line) - 1:
                        data[y + 1][x + 1] = "|"
                        worldlines[y + 1][x + 1] += worldlines[y][x]
        # print(f"{''.join(line)} -- splits: {s}")
    logging.info(f"star 2: {sum(worldlines[-1])}")

    # for y, line in enumerate(worldlines):
    #     for x, c in enumerate(line):
    #         if data[y][x] == "^":
    #             print("^ ", end="")
    #         elif c == 0:
    #             print("  ", end="")
    #         else:
    #             print(f"{c} ", end="")
    #     print("--", sum(line))


star1(data)
star2(data2)
