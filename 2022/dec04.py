import os

runtest = False
stardate = "04"
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


def makerange(s: str) -> set:
    result = set()
    start, end = [int(_) for _ in s.split("-")]
    for _ in range(start, end+1):
        result.add(_)
    return result


def star1():
    result = 0
    for _ in data:
        e1, e2 = [makerange(_) for _ in _.split(",")]
        inters = e1 & e2
        if inters == e1 or inters == e2:
            result += 1
        # print(_, e1, e2, e1 & e2)
    return result


def star2() -> int:
    result = 0
    for _ in data:
        e1, e2 = [makerange(_) for _ in _.split(",")]
        if len(e1 & e2) > 0:
            result += 1
        # print(_, e1, e2, e1 & e2)
    return result


print("star1:", star1())
print("star2:", star2())

# https://adventofcode.com/2022/day/4
