from collections import defaultdict
from datetime import time

#print(1000000000 % 60); exit()

start = "abcdefghijklmnop";inp = open('16.txt').read().split(",")
#start = "bfcdeakhijmlgopn"
#start = "abcde"; inp = ['s1', 'x3/4', 'pe/b'];d=2
L = len(start)
a=initial=list(start)
#0: abcde
#1: baedc
#2: ceadb
SPIN = 0
EXCHANGE = 1
PARTNER = 2

def parse(text):
    res = []
    cm = {'p': "<<", 'x': "----", 's': "xxxxxxx"}
    for m in text:
        c = m[0]
        #print(cm[c])
        if c == "s":  # spin
            tail = int(m[1:])
            res.append([SPIN, tail])
        elif c == "x": # exchange
            x, y = map(int, m[1:].split("/"))
            res.append([EXCHANGE, x, y])
        elif c == "p": # partner swap
            x, y = m[1:].split("/")
            res.append([PARTNER, x, y])
    return res

code = parse(inp)

def codeinsight(code):
    print("code", len(code))
    c = defaultdict(int)
    bs = defaultdict(int)
    opt = g = 0
    for m in code:
        if m[0] != 0: opt += 1
        else: print(opt); bs[opt] += 1; opt = 0; g += 1
        c[m[0]] += 1
    print(bs, g, c)

def runcode(ops, arr):
    for m in code:
        op = m[0]
        if not op in ops:
            continue
        if op == SPIN:
            tail = m[1]
            arr = arr[-tail:] + arr[0:-tail]
        elif op == EXCHANGE:
            x, y = m[1:]
            #print(x, y)
            arr[x], arr[y] = arr[y], arr[x]
        elif op == PARTNER:
            x, y = [arr.index(c) for c in m[1:]]
            arr[x], arr[y] = arr[y], arr[x]
    return arr

print(a, inp, code)

def dancers(arr):
    r = ""
    for c in arr:
        r += "" + c
    return r


print("{:2} {}".format(0, dancers(a)))
#a = runcode([PARTNER], a)
print("{:3} {}".format(0, dancers(a)))
#exit()
i = 0
while 1:
    offset = 0
    a = runcode([SPIN, EXCHANGE], a)
    a = runcode([PARTNER], a)

    i+=1
    #print(i, a)

    if i % 100 == 0:
        print("{:3} {}".format(i, dancers(a)))
    #if i == 200: break

print("padheomkgjfnblic")

#abcdef
#defabc offset 3
#x 1, 4 => x 4, 7 => x 4, 1

exit()
m = [a.index(c) for c in start]
print(m)

for i in range(d):
    b = [a[t] for t in m]
    a = b
    print(a)

r = ""
for c in a:
    r += c
print(r)