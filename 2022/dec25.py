from collections import defaultdict
import os

runtest = False
stardate = 25
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


def decode(s) -> int:
    values = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2
    }
    return sum(values[c] * (5 ** p) for p, c in enumerate(s[::-1]))


snafu = {
    0: "0",
    1: "1",
    2: "2",
    3: "=",
    4: "-"
}


def encode(n):
    if n == 0:
        return ""
    d, r = divmod(n, 5)
    if r in [3, 4]:
        d += 1
    return encode(d) + snafu[r]


def star1():
    n = sum(decode(_) for _ in data)
    return encode(n)


print("star1:", star1())
