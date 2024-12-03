import logging
import re

from reader import get_data, set_logging, timeit

runtest = False
stardate = "03"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    result = 0
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    for s in data:
        for x in pattern.findall(s):
            result += int(x[0]) * int(x[1])
    print(result)


@timeit
def star2(data):
    logging.debug("running star 2")
    result = 0
    pattern = re.compile(r"mul\((\d+),(\d+)\)|(don't\(\))|(do\(\))")
    enabled = True
    for s in data:
        for x in pattern.findall(s):
            if "don't()" in x:
                enabled = False
                continue
            if "do()" in x:
                enabled = True
                continue
            if enabled:
                result += int(x[0]) * int(x[1])
    print(result)


star1(data)
star2(data2)
