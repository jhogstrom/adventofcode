import os

runtest = False
stardate = 25
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


def decode(s) -> int:
    return sum(("=-012".index(c)-2) * (5 ** p) for p, c in enumerate(s[::-1]))


def encode(n):
    if n == 0:
        return ""
    d, r = divmod(n, 5)
    if r in [3, 4]:
        d += 1
    return encode(d) + "012-="[r]


def star1():
    n = sum(decode(_) for _ in data)
    return encode(n)


print("star1:", star1())
