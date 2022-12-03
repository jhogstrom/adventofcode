import os

runtest = False
stardate = "03"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

if not data:
    raise FileNotFoundError(f"No data in {dataname}")


def calc(s) -> int:
    res = 0
    for _ in s:
        if _ > "a":
            res += ord(_) - ord("a") + 1
        else:
            res += ord(_) - ord("A") + 27
    return res


def star1():
    score = 0
    for _ in data:
        c1 = set(_[:int(len(_)/2)])
        c2 = set(_[int(len(_)/2):])
        score += calc(c1 & c2)
    return score


def star2():
    score = 0
    for _ in range(0, len(data), 3):
        e1 = set(data[_])
        e2 = set(data[_ + 1])
        e3 = set(data[_ + 2])
        score += calc(e1 & e2 & e3)
    return score


print("star1", star1())
print("star2", star2())
# https://adventofcode.com/2022/day/3
