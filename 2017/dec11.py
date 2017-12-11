from collections import defaultdict

inp = open('11.txt').read().split(",")
#inp = ["ne","ne","ne"] #3
#inp = ["ne","ne","sw","sw"] #0
#inp = ["ne","ne","s","s"] #2
#inp = ["se","sw","se","sw","sw"] # is 3 steps away
ms = defaultdict(int)
N = "n"
S = "s"
SE = "se"
SW = "sw"
NE = "ne"
NW = "nw"
W = "w"
E = "e"

print(inp)

def dist():
    north = ms[N] - ms[S]
    ne = ms[NE] - ms[SW]
    nw = ms[NW] - ms[SE]
    n2 = north + ne/2 + nw/2
    east = ms[NE] + ms[SE] - ms[NW] - ms[SW]
    steps = abs(east) + n2 - abs(east/2)
    return steps

steps = 0
for m in inp:
    ms[m] += 1
    steps = max(steps, dist())

print(steps)