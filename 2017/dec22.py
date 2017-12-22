from collections import defaultdict

#inp = [l.strip() for l in open('dec22ex.txt')]
inp = [l.strip() for l in open('22.txt')]
#print(inp)

m = defaultdict(int)

def coord(x, y): return "{};{}".format(x, y)

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

for y in range(len(inp)):
    for x in range(len(inp[y])):
        if inp[y][x] == "#":
            m[coord(x, y)] = INFECTED

x = y = len(inp) // 2
print(x, y)
UP = [0,-1]; DOWN = [0,1]; LEFT = [-1, 0]; RIGHT = [1, 0]
directions = [UP, RIGHT, DOWN, LEFT]
d = infected = 0

turnmap = { CLEAN: 3, WEAKENED: 0, INFECTED: 1, FLAGGED: 2}
transitionmap = {CLEAN: WEAKENED, WEAKENED: INFECTED, INFECTED: FLAGGED, FLAGGED: CLEAN}

for i in range(10000000):
    if i % 10000 == 0: print(i)
    c = coord(x,y)
    d = (d + turnmap[m[c]]) % 4
    m[c] = transitionmap[m[c]]
    if m[c] == INFECTED:
        infected += 1

    x += directions[d][0]
    y += directions[d][1]

print(infected)

#Answer: 5259