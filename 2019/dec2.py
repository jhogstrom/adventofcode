import os

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\2.txt'

prgdata = open(filename, 'r').readline()
#prgdata = "1,0,0,0,99"
#prgdata = "2,3,0,3,99"
#prgdata = "2,4,4,5,99,0"
#prgdata = "1,1,1,4,99,5,6,0,99"
#prgdata = "1,9,10,3,2,3,11,0,99,30,40,50"
prg = [int(_) for _ in prgdata.split(",")]
print(prg)

#prg[1] = 12
#prg[2] = 2

def add(p1, p2):
    return p1 + p2

def mul(p1, p2):
    return p1 * p2

def getop(opcode):
    ops = { 1: add, 2: mul}
    #print(f"opcode: {opcode}")
    return ops[opcode]

def runprg(progx, i1, i2):
    prog = [_ for _ in progx]
    prog[1] = i1
    prog[2] = i2

    ptr = 0
    while prog[ptr] != 99:
        op = getop(prog[ptr])
        res = op(prog[prog[ptr+1]], prog[prog[ptr+2]])
        #print(f"res: {res} => {prg[ptr+3]}")
        prog[prog[ptr+3]] = res
        ptr += 4
    #print(prog)
    return prog[0]

#maxi1, maxi2, target = 13, 3, 5098658
maxi1, maxi2, target = 100, 100, 19690720
for inp1 in range(0, maxi1):
    for inp2 in range(0, maxi2):
        prg = [int(_) for _ in prgdata.split(",")]
        res = runprg(prg, inp1, inp2)
        if inp1 == 12 and inp2 == 2:
            print(f"{inp1}-{inp2} => {res}")
        if res == target:
            print(f"{inp1}/{inp2} => {res} -- {100 * inp1 + inp2}")
            break


