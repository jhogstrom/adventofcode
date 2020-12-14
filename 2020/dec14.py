import os
import itertools
from timing import timeit
import enum

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]


def star1():
    mask = 0
    regs = {}
    mask = ""
    for s in data:
        cmd, d = s.split(" = ")
        if cmd == "mask":
            mask = d
        else:
            mem = cmd[4:-1]
            v = f"{int(d):036b}"
            r = ""
            for i, m in enumerate(mask):
                if m in "10":
                    r += m
                else:
                    r += v[i]
            regs[mem] = int(r, 2)
    return(sum(regs.values()))

def star2():
    mask = 0
    regs = {}
    m = ""
    for s in data:
        cmd, d = s.split(" = ")
        if cmd == "mask":
            mask = d
        else:
            mem = cmd[4:-1]
            v = f"{int(mem):036b}"
            floatingmem = []
            for i, m in enumerate(mask):
                if m in "1X":
                    floatingmem.append(m)
                else:
                    floatingmem.append(v[i])
            
            xcount = len([_ for _ in floatingmem if _ == "X"])

            for f in range(2**xcount):
                bits = f"{f:0{xcount}b}"
                newmem = []
                xindex = 0
                for c in floatingmem:
                    if c == "X":
                        c = bits[xindex]
                        xindex += 1
                    newmem.append(c)
                newmem = ''.join(newmem)
                regs[newmem] = d

    return(sum([int(_) for _ in regs.values()]))

# data = [
# "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
# "mem[8] = 11",
# "mem[7] = 101",
# "mem[8] = 0"

# ]

# data = [
#     "mask = 000000000000000000000000000000X1001X",
# "mem[42] = 100",
# "mask = 00000000000000000000000000000000X0XX",
# "mem[26] = 1"
# ]


print(f"* {star1()}")
print(f"** {star2()}")
# star2()