import os
import logging

runtest = False
stardate = "01"
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"
levels = {
    True: logging.DEBUG,
    False: logging.INFO
}
logging.basicConfig(level=levels[runtest], format="%(message)s")

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()
# data = data[:10]

def star1():
    res = 0
    for _ in data:
        d = [c for c in _ if c.isdigit()]
        res += int(d[0]+d[-1])

    print(res)

def star2():
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven":"7",
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
    print("not 54970")

# star1()
star2()