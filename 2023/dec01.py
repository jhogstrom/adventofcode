import logging
from reader import get_data, set_logging, timeit


runtest = False
stardate = "1"
data = get_data(stardate, runtest)
set_logging(runtest)


@timeit
def star1():
    res = 0
    for _ in data:
        logging.debug(f"_ {_}")
        d = [c for c in _ if c.isdigit()]
        logging.debug(d)
        res += int(d[0]+d[-1])

    print(res)


@timeit
def star2():
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven" :"7",
        "eight": "8",
        "nine": "9"
    }
    res = 0
    for _ in data:
        logging.debug(f"_ {_}")
        r = ""
        for i in range(len(_)):
            found = False
            for n in numbers:
                if n in _[i:min(i+len(n), len(_))]:
                    logging.debug(f"replacing {n} with {numbers[n]}")
                    r += numbers[n]
                    found = True
                    break
            if not found:
                r += _[i]

        d = [c for c in r if c.isdigit()]
        logging.debug(r)
        logging.debug(f"{d}  {int(d[0]+d[-1])}")
        res += int(d[0]+d[-1])

    print(res)


star1()
star2()
