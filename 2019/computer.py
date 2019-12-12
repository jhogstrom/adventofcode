class intcomputer:
    def __init__(self, prog, param_array = [], name = None):
        self.prog = prog
        self.pptr = 0
        self._terminated = False
        self._waiting = False
        self.input = param_array
        self.debug = False
        self.result = 0
        if name:
            self.name = name
        else:
            self.name = "NONAME"
        self.relativebase = 0
        self.outputarray = []
        print(f"Creating {self.name}({param_array})")

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

    def execute(self, p=None):
        if not p is None:
            self.add_input(p)
        while (not self._terminated) and (not self._waiting):
            op = self.getop()
            op()
            #print(self)

        res = ""

        if self._terminated:
            res += f" >> TERMINATED -- @ {self.pptr}<<"
        if self._waiting:
            res += f" >> WAITING -- @ {self.pptr}<<"
        #print(res)
        return self
        
    def step(self):
        self.pptr += 1

    def pop_output(self):
        assert(len(self.outputarray) > 0)
        res = self.outputarray[0]
        self.outputarray = self.outputarray[1:]
        return res

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
        #print(f">>> {p1}")
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

if __name__ == "__main__":
    print("Running the wrong module!", __file__)