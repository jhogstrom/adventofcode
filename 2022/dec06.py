from collections import defaultdict
import os

runtest = False
stardate = "06"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


def star(s, size):
    for i in range(len(s)):
        if len(set(s[i:i+size])) == size:
            return i+size
    raise ValueError


print("star1", star(data[0], 4))
print("star1", star(data[0], 14))
