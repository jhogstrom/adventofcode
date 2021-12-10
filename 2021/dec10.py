import os
from timer import timeit
from collections import defaultdict, deque

stardate = 10
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]

scoremap = {
    "": 0,
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def validate_string(s: str):
    org = s[:]
    slen = len(s)
    s = s.replace("{}", "").replace("()", "").replace("[]", "").replace("<>", "")
    while slen != len(s):
        slen = len(s)
        s = s.replace("{}", "").replace("()", "").replace("[]", "").replace("<>", "")
        # print(s)

    missing = ""
    for i, c in enumerate(s):
        if c in ")]}>":
            missing = c
            break
    score = scoremap[missing]
    # if score > 0:
    #     print(org, "->", s, end="")
    #     print(f"  score: {score} (missing '{missing}'")
    return score, s


@timeit
def star1(data):
    res = 0
    for d in data:
        v, _ = validate_string(d)
        res += v
    print(res)

closing_map = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def complete_string(s: str) -> int:
    res = ""
    stack = [" "]
    for c in s[::-1]:
        if c in "([{<":
            if stack[-1] == closing_map[c]:
                stack.pop()
            else:
                res += closing_map[c]
        if c in closing_map.values():
            stack.append(c)
    return res


scoring = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}
def score_string(s: str) -> int:
    res = 0
    for c in s:
        res *= 5
        res += scoring[c]
    return res

@timeit
def star2(data):
    scores = []
    for d in data:
        v, s = validate_string(d)
        if v != 0:
            continue
        completed = complete_string(s)
        res = score_string(completed)
        scores.append(res)
        # print(f"{d} -> {s} ({v}) ==> {completed}")

    scores = sorted(scores)
    # print(scores)
    # print(len(scores)//2)
    print(scores[(len(scores) // 2)])

star1(data)
star2(data)
