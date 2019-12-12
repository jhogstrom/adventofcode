import os

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec5.txt'

prgdata = open(filename, 'r').readline()
#prgdata = "1,0,0,0,99"
#prgdata = "2,3,0,3,99"
#prgdata = "2,4,4,5,99,0"
#prgdata = "1,1,1,4,99,5,6,0,99"
#prgdata = "1,9,10,3,2,3,11,0,99,30,40,50"
prg = [int(_) for _ in prgdata.split(",")]
#print(prg)

#prg[1] = 12
#prg[2] = 2

def add(params, inputs):
    assert(len(params) == 2)
    return params[0] + params[1]

def mul(params, inputs):
    assert(len(params) == 2)
    return params[0] * params[1]

def saveparam(params, inputs):
    return inputs[0]

def outputparam(params, inputs):
    print(len(params))
    assert(len(params) == 1)
    print(f"OUTPUT: {params[0]}")
    return None

def getmodes(opcode, pcount):
    modes = str(opcode[:-2]).zfill(pcount+1)[::-1]
    #print(f"modes: {modes}/{pcount} - {[int(_) for _ in modes]}")
    return [int(_) for _ in modes]

def getop(opcode):
    ops = { 
        1: (add, 2), 
        2: (mul, 2), 
        3: (saveparam, 1), 
        4: (outputparam, 1) 
    }
    res = ops[int(opcode) % 100]
    modes = getmodes(opcode, res[1])
    return res + tuple([modes])

def getvalue(prog, mode, ptr):
    #modes = ["position", "immediate"]
    if mode == 0: # Position
        res = int(prog[int(prog[ptr])])
    else: # Immediate
        res = int(prog[ptr])

    #print(f"ptr: {ptr} mode: {modes[mode]}({mode}) res: {res} prog[{ptr}]={prog[ptr]}")
    return res

def getposition(prog, mode, ptr):
    modes = ["position", "immediate"]
    if mode == 0: # Position
        res = int(prog[ptr])
    else: # Immediate
        res = prog[ptr]

    #print(f"ptr: {ptr} mode: {modes[mode]}({mode}) res: {res} prog[{ptr}]={prog[ptr]}")
    return res


def runprg(progx, inputs):
    prog = [_ for _ in progx]
    #print(prog)

    ptr = 0
    while int(prog[ptr]) % 100 != 99:
        instr = prog[ptr]
        op, pcount, modes = getop(instr)
        #print("pcount: ", pcount)
        params = []
        ptr += 1
        for m in range(pcount):
            params.append(getvalue(prog, m, ptr))
            ptr += 1

        #print(f"{op.__name__}({params}) - {ptr} {prog}")
        res = op(params, inputs)
        if op in [mul, add]:
            storage = getposition(prog, modes[pcount], ptr)
            ptr += 1
            prog[storage] = str(res)
        elif op == outputparam:
            r = getvalue(prog, modes[pcount], ptr)
            print(f"OUTPUT: {r}")
        elif op == saveparam:
            storage = getposition(prog, modes[pcount], ptr)
            prog[storage] = str(res)

    return prog[0]


def teststuff():
#    op, pcount, modes = getop("0101")
#    print(op.__name__, pcount, modes)
    runprg("1002,4,3,4,33".split(","), [1])
    runprg("1002,4,3,4,33".split(","), [1])
    runprg("4,1,99".split(","), [1])
    exit()  

teststuff()

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


