import json
import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "12"
year = "2015"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")


def scan_element(element):
    if isinstance(element, int):
        return element
    elif isinstance(element, str):
        return 0
    elif isinstance(element, list):
        return sum(scan_element(e) for e in element)
    elif isinstance(element, dict):
        if "red" in element.values():
            return 0
        return sum(scan_element(e) for e in element.values())
    else:
        return 0


@timeit
def star2(data):
    logging.debug("running star 2")
    doc = json.loads(data[0])
    res = scan_element(doc)
    print(res)


star1(data)
star2(data2)
