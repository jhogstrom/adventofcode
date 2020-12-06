import os
import itertools
import time

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec5.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

def id_for_card(s: str) -> int:
    return int(s.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2)

ids = sorted([id_for_card(_) for _ in data])
print("* ", ids[-1])

delta = ids[0]
for ix, id in enumerate(ids):
    if id - ix != delta:
        print("**", id-1)
        break

