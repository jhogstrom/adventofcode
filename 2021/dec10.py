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
    slen = len(s)
    s = s.replace("{}", "").replace("()", "").replace("[]", "").replace("<>", "")
    while slen != len(s):
        slen = len(s)
        s = s.replace("{}", "").replace("()", "").replace("[]", "").replace("<>", "")

    missing = ""
    for c in s:
        if c in scoremap:
            missing = c
            break
    score = scoremap[missing]
    return score, s


@timeit
def star1(data):
    # Here we're only interested in the first item in the resulting tuple (int, str)
    res = sum(validate_string(_)[0] for _ in data)
    print(res)


closing_map = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


def complete_string(s: str) -> int:
    res = []
    stack = [" "]
    for c in s[::-1]:
        if c in closing_map:
            if stack[-1] == closing_map[c]:
                stack.pop()
            else:
                res.append(closing_map[c])
        if c in closing_map.values():
            stack.append(c)
    return res


scoring = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def score_completion_chars(completion_chars) -> int:
    res = 0
    for c in completion_chars:
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
        scores.append(score_completion_chars(complete_string(s)))

    scores = sorted(scores)
    print(scores[(len(scores) // 2)])


star1(data)
star2(data)
