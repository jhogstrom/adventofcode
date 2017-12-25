h = 0
for b in range(108400, 125400+1, 17):
  #for d in range(2, b):
    for e in range(2, b):
      if b % e == 0:
          h += 1
          break

print(h)
exit()

h = 0
for x in range(108400,125400 + 1,17):
    for i in range(2,x):
        if x % i == 0:
            h += 1
            break
print(h)
exit()
from collections import defaultdict

inp=[l.strip() for l in open('23.txt')]

print(inp)

pp = 0
regs = defaultdict(int)
regs['a'] = 1

#set X Y sets register X to the value of Y.
#sub X Y decreases register X by the value of Y.
#mul X Y sets register X to the result of multiplying
## the value contained in register X by the value of Y.
#jnz X Y jumps with an offset of the value of Y, but
# only if the value of X is not zero. (An offset of
#  2 skips the next instruction, an offset of -1
#  jumps to the previous instruction, and so on.)
def value(v):
#    if type(v) == int: return v
    if v in "abcdefgh":
        return regs[v]
    return int(v)

m = 0
i = 0
#24696670000 3087065948 17 defaultdict(<class 'int'>, {'a': 1, 'b': 108400, 'c': 125400, 'f': 0, 'd': 28480, 'e': 107705, 'g': 3067301520})

#h = 1000
#regs = {'a': 1, 'b': 108400 + h * 17, 'c': 125400, 'd': 48, 'e': 108400 + h * 17, 'f': 0, 'g': 0, 'h': h}; pp = 23

def jumpstart():
    i = 24696670000; pp = 17; regs = {'a': 1, 'b': 108400, 'c': 125400, 'f': 0, 'd': 28480, 'e': 107705, 'g': 3067301520}

while pp < len(inp):
    i += 1
    l = inp[pp].split()
    ins = l[0]
    if ins == "set":
        regs[l[1]] = value(l[2])
    if ins == "sub":
        regs[l[1]] -= value(l[2])
    if ins == "mul":
        regs[l[1]] *= value(l[2])
        m += 1
    if ins == "jnz":
        if value(l[1]) != 0:
            if pp in [23, 24, 28, 29, 32]:
                print("JUMP {:15} {:2} {} ({})".format(inp[pp], pp, regs, i))
            pp += value(l[2])
            continue
        else:
            print("NOJU {:15} {:2} {} ({})".format(inp[pp], pp, regs, i))
            #if pp == 4:
#    print("{:15} {:2} {}".format(inp[pp], pp, regs))
    pp += 1
    #    exit()
    if i == 40000000: exit()

print(m, regs['h'])
# 1000 is too high