import json
import os

runtest = False
stardate = "13"
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


def make_list(o) -> list:
    return o if isinstance(o, list) else [o]


def comp(left, right) -> int:
    if left == right:
        return 0
    if left < right:
        return -1
    return 1


def compare(left, right, level=0) -> int:
    # print(f"{'-'*level}comparing {left} <= {right}")
    if isinstance(left, int) and isinstance(right, int):
        return comp(left, right)

    if isinstance(left, list) and isinstance(right, list):
        c = 0
        while min([c, len(left)-1, len(right)-1]) == c:
            lval = left[c]
            rval = right[c]
            # print(f"{'-'*level}item {c}: {lval} <-> {rval}")
            res = compare(lval, rval, level+1)
            if res != 0:
                return res
            c += 1
        # print(f"{'-'*level}Tiebreaker on length")
        return comp(len(left), len(right))

    return compare(make_list(left), make_list(right), level+1)


def star1():
    res = []
    for ix, i in enumerate(range(0, len(data), 3), 1):
        left = json.loads(data[i])
        right = json.loads(data[i+1])
        if compare(left, right) == -1:
            res.append(ix)

    return sum(res)


def star2():
    c1, c2 = [[2]], [[6]]
    packets = [json.loads(_) for _ in data if _]
    packets.extend([c1, c2])
    for i in range(len(packets)-1):
        for j in range(len(packets)-i-1):
            if compare(packets[j], packets[j+1]) == 1:
                packets[j], packets[j+1] = packets[j+1], packets[j]

    return (packets.index(c1) + 1) * (packets.index(c2) + 1)


print("star1", star1())
print("star2", star2())
