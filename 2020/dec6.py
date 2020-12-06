import os
import itertools
import time

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec6.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()] + [""]

# data = [
#     "abc",
#     "",
#     "a",
#     "b",
#     "c",
#     "",
#     "ab",
#     "ac",
#     "",
#     "a",
#     "a",
#     "a",
#     "a",
#     "", "", "", ""
#     "b"
#     ]

def get_record(data):
    res = []
    for s in data:
        if s != "":
            res.append(s)
        else:
            if res != [""] and res != []:
                yield res
            res = []

    if res != [] and res != [""]:
        yield res


def star1():
    count = 0
    for rec in get_record(data):
        answers = set()
        for s in rec:
            answers.update(set(s))
        count += len(answers)
    print(f"* {count}")


def star2():
    count = 0
    for rec in get_record(data):
        answers = set(rec[0])
        for s in rec[1:]:
            answers &= set(s)
        count += len(answers)

    print(f"** {count}")

star1()
star2()

