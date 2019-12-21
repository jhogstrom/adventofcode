import os
import itertools
from computer import intcomputer

curdir = os.path.dirname(os.path.abspath(__file__))

class _intcomputer:
    def __init__(self, prog, input = [], name = None):
        self.prog = prog
        self.pptr = 0
        self._terminated = False
        self._waiting = False
        self.input = input
        self.debug = False
        self.result = 0
        if name:
            self.name = name
        else:
            self.name = "NONAME"
        self.relativebase = 0
        self.outputarray = []
        print(f"Creating {self.name}({input})")

    def __str__(self):
        res = []
        for i in range(len(self.prog)):
            if i == self.pptr:
                if not self._terminated:
                    op = self.map_operation(self.prog[i])
                    res.append(f"[{self.pptr}:>>{self.op_name(op)}:{self.prog[i]}]")
                else:
                    res.append(f"[{self.prog[i]}]")
            else:
                res.append(self.prog[i])

        res = str(res) # str(res[self.pptr:self.pptr+5])
        if self._terminated:
            res += " >> TERMINATED <<"
        if self._waiting:
            res += " >> WAITING <<"
        return res

    def printop(self, pcount):
        return
        addr = self.pptr - 1
        regs = self.prog[addr:addr+pcount+1]
        op = self.map_operation(self.prog[addr])
        pmodes = self._modes[::-1]
        res = f"[{addr}::]{self.op_name(op)} /{pmodes[:pcount]}/:{self.prog[addr]} "
        addr += 1
        for p in range(pcount):
            res += f"{self.prog[addr+p]}"
            if pmodes[p] == "0":
                self.extend_memory(self.prog[addr+p])
                res += f"->{self.prog[self.prog[addr+p]]}"
            elif pmodes[p] == "2":
                a = self.prog[addr+p] + self.relativebase
                self.extend_memory(a)
                res += f"=({self.relativebase}->{a})=>{self.prog[a]}"

            res += " "
        print(f"{res} -- {regs}")

    def log(self, s):
        if self.debug:
            print(s)

    def execute(self):
        while (not self._terminated) and (not self._waiting):
            op = self.getop()
            op()
            #print(self)

        res = ""

        if self._terminated:
            res += f" >> TERMINATED -- @ {self.pptr}<<"
        if self._waiting:
            res += f" >> WAITING -- @ {self.pptr}<<"
        print(res)
        return self
        
    def step(self):
        self.pptr += 1

    def map_operation(self, opcode):
        ops = { 
            1: self.add, 
            2: self.mul, 
            3: self.store,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.adjust_relative_base,
            99: self.terminate }
        op = opcode % 100
        try:
            return ops[op]
        except KeyError:
            print(f"Attempting to map operation {opcode}")

    def op_name(self, op):
        return str(op).split(" ")[2].split(".")[1]

    def getop(self):
        instr = self.getvalue()
        op = self.map_operation(instr)
        opcode = str(instr)
        self._modes = opcode[:-2].zfill(3)
        return op

    def add_input(self, v):
        self.input.append(v)
        self._waiting = False
    
    def write(self, addr, v):
        self.extend_memory(addr)
        self.prog[addr] = v

    def extend_memory(self, ptr):
        while len(self.prog) <= ptr:
            self.prog.append(0)

    def getvalue(self):
        res = self.prog[self.pptr]
        self.step()
        #print(f"*{res} - immediate parameter {self.pptr-1}")
        return res

    def dereference(self, addrmode):
        ptr = self.prog[self.pptr]
        self.extend_memory(ptr)
        self.step()
        if addrmode:
            return ptr
        return self.prog[ptr]

    def getrelativevalue(self, addrmode=False):
        p1 = self.prog[self.pptr]
        addr = p1 + self.relativebase
        self.extend_memory(addr)
        self.step()
        if addrmode:
            return addr

        assert(addr >= 0) # Python will treat negative numbers as back of list...
        return self.prog[addr]

    def get_parameter(self, addrmode=False):
        nextmode = int(self._modes[-1:])
        self._modes = self._modes[:-1]
        if addrmode:
            assert(nextmode != 1)
        if nextmode == 0: # Position mode
            return self.dereference(addrmode=addrmode)

        if nextmode == 1: # Immediate mode
            return self.getvalue()

        if nextmode == 2: # Relative mode
            return self.getrelativevalue(addrmode=addrmode)
        
        raise NotImplementedError(f"Illegal mode {nextmode}")

    def add(self): # op 01
        self.printop(3)
        p1 = self.get_parameter()
        p2 = self.get_parameter()
        addr = self.get_parameter(addrmode=True)
        self.log(f"add({p1}, {p2}) => {addr}")
        self.write(addr, p1 + p2)

    def mul(self): # op 02
        self.printop(3)
        p1 = self.get_parameter()
        p2 = self.get_parameter()
        addr = self.get_parameter(addrmode=True)
        self.log(f"mul({p1}, {p2}) => {addr}")
        self.write(addr, p1 * p2)
      
    def store(self): # op 03
        self.printop(1)
        if len(self.input) == 0:
            self._waiting = True
            self.pptr -= 1
            return 
        addr = self.get_parameter(addrmode=True)
        val = self.input[0]
        self.input = self.input[1:]
        self.log(f"store({val}) => {addr}")
        self.write(addr, val)

    def output(self): # op 04
        self.printop(1)
        p1 = self.get_parameter()
        print(f">>> {p1}")
        self.result = p1
        self.outputarray.append(p1)

    def jump_if_true(self): # op 05
        self.printop(2)
        p1 = self.get_parameter()
        addr = self.get_parameter()
        if p1 != 0:
            assert(len(self.prog) >= addr)
            self.pptr = addr
        self.log(f"JNZ({p1}) => {addr}")
        
    def jump_if_false(self): # op 06
        self.printop(2)
        p1 = self.get_parameter()
        addr = self.get_parameter()
        if p1 == 0:
            assert(len(self.prog) >= addr)
            self.pptr = addr
        self.log(f"JZ({p1}) => {addr}")

    def less_than(self): # op 07
        self.printop(3)
        RESULT = {True: 1, False: 0}
        p1 = self.get_parameter()
        p2 = self.get_parameter()
        addr = self.get_parameter(addrmode=True)
        self.write(addr, RESULT[p1 < p2])
        self.log(f"LT({p1}, {p2}) => {addr}")

    def equals(self): # op 08
        self.printop(3)
        RESULT = {True: 1, False: 0}
        p1 = self.get_parameter()
        p2 = self.get_parameter()
        addr = self.get_parameter(addrmode=True)
        self.write(addr, RESULT[p1 == p2])
        self.log(f"EQ({p1}, {p2}) => {addr}")

    def adjust_relative_base(self): # op 09
        self.printop(1)
        p1 = self.get_parameter()
        oldbase = self.relativebase
        self.relativebase += p1
        self.log(f"REBASE({p1}) ==> {oldbase} > {self.relativebase}")
        assert(self.relativebase >= 0)

    def terminate(self): # op 99
        self._terminated = True

def runprog(prg, noun, verb):
    prg[1] = noun
    prg[2] = verb
    return intcomputer(prg).execute().prog[0]


def dec2_star1():
    filename = f'{curdir}\\dec2.txt'
    prgdata = open(filename, 'r').readline()

    prg = [int(_) for _ in prgdata.split(",")]
    print(f"star1: {runprog(prg, 12, 2)} {prg[0]}")


def dec2_star2():
    filename = f'{curdir}\\dec2.txt'
    prgdata = open(filename, 'r').readline()

    maxi1, maxi2, target = 100, 100, 19690720
    for inp1 in range(0, maxi1):
        for inp2 in range(0, maxi2):
            prg = [int(_) for _ in prgdata.split(",")]
            if runprog(prg, inp1, inp2) == target:
                print(f"{inp1}/{inp2} => {target} --> {100 * inp1 + inp2}")
                return

def dec5_star1():
    filename = f'{curdir}\\dec5.txt'
    prgdata = open(filename, 'r').readline()
    prg = [int(_) for _ in prgdata.split(",")]
    intcomputer(prg, input = [1]).execute()

def dec5_star2():
    filename = f'{curdir}\\dec5.txt'
    prgdata = open(filename, 'r').readline()
    prg = [int(_) for _ in prgdata.split(",")]
    c = intcomputer(prg, input = [5]).execute()
    print(f"Result: {c.result}")

def dec7_star1():
    #prgdata = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    #prgdata = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    #prgdata = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    seq = [0,1,2,3,4]
    perms = itertools.permutations(seq)
    maxres = None
    for p in perms:
        A = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[0], 0], name="A").execute()
        B = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[1], A.result], name="B").execute()
        C = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[2], B.result], name="C").execute()
        D = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[3], C.result], name="D").execute()
        E = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[4], D.result], name="E").execute()
        if not maxres or E.result > maxres:
            maxres = E.result
            setting = p
                        
    print(f"Max: {maxres}/{setting}")

def dec7_star2():
    #prgdata = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    #prgdata = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

    seq = [5,6,7,8,9]
    perms = itertools.permutations(seq)
    maxres = None
    for p in perms:
        A = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[0]], name="A")
        B = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[1]], name="B")
        C = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[2]], name="C")
        D = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[3]], name="D")
        E = intcomputer([int(_) for _ in prgdata.split(",")], input=[p[4]], name="E")

        computers = [A, B, C, D, E]
        c = 0
        while not any([_._terminated for _ in computers]):
            computers[c].add_input(computers[(c-1 + 5) % 5].result)
            computers[c].execute()
            c = (c+1) % 5

        print(p)

        if not maxres or E.result > maxres:
            maxres = E.result
            setting = p
                        
    print(f"Max: {maxres}/{setting}")

def dec9_star1():
    prgdata = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    prgdata = "1102,34915192,34915192,7,4,7,99,0"
    prgdata = "104,1125899906842624,99"
    filename = f'{curdir}\\dec9.txt'
    prgdata = open(filename, 'r').readline()

    #prgdata = "03,0,99"
    #prgdata = "109,100,203,5,99"
    #prgdata = "1005,2,5,04,1,99"
    #prgdata = "2002,4,10,0,99"
    #prgdata = "109,3,2207,2,4,7,99,04,6,99"
    #prgdata = "109,3,209,4,2201,-2,-3,1,99"
    #prgdata = "109,1,203,1,203,1,99"
    #prgdata = "109,1,2208,3,4,0,99,99"
    #prgdata = "003,3,99,3"
    #prgdata = "103,3,99,3"
    #prgdata = "109,2,203,3,99,3"

    prg = [int(_) for _ in prgdata.split(",")]    
    computer = intcomputer(prg, input = [1]).execute() 
    print([int(_) for _ in prgdata.split(",")])
    print(computer.prog)
    print(computer.outputarray)

def dec9_star2():
    filename = f'{curdir}\\dec9.txt'
    prgdata = open(filename, 'r').readline()

    prg = [int(_) for _ in prgdata.split(",")]    
    computer = intcomputer(prg, input = [2]).execute() 
#    print([int(_) for _ in prgdata.split(",")])
    print(computer.outputarray)



dec2_star1()
#dec2_star2()
#dec5_star1()
#dec5_star2()
#dec9_star1()
#dec9_star2()

