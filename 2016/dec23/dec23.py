class Memory:
    def __init__(self, code = None) -> None:
        self.code = code or []

    def get_instruction(self, addr: int) -> str:
        return self.code[addr]

    def set_instruction(self, addr: int, instr: str) -> None:
        self.code[addr] = instr



class Cpu:
    def __init__(self, memory) -> None:
        self.pc = 0
        self.memory = memory
        self.bps = []
        self.regs = {
            "a": 12,
            "b": 0,
            "c": 0,
            "d": 0,
        }

    def add_breakpoint(self, bp):
        self.bps.append(bp)

    def is_breakpoint(self, line) -> str:
        ismatch = False
        if isinstance(line, str):
            p = line.split()
            ismatch = p[0] in self.bps

        return self.pc in self.bps or line in self.bps or ismatch

    def get_operation(self, instr: str):
        if instr == "cpy":  # 2 args
            return self.op_cpy

        if instr == "inc":  # 1 args
            return self.op_inc

        if instr == "dec":  # 1 args
            return self.op_dec

        if instr == "jnz":  # 2 args
            return self.op_jnz

        if instr == "tgl":  # 1 args
            return self.op_tgl

        raise ValueError(instr)

    def get_value(self, v) -> int:
        return self.regs[v] if v in "abcd" else int(v)

    def op_cpy(self, *params):
        if params[1] in "abcd":
            value = self.get_value(params[0])
            self.regs[params[1]] = value
        self.pc += 1

    def op_inc(self, *params):
        if params[0] in "abcd":
            self.regs[params[0]] += 1
        self.pc += 1

    def op_dec(self, *params):
        if params[0] in "abcd":
            self.regs[params[0]] -= 1
        self.pc += 1

    def op_jnz(self, *params):
        value = self.get_value(params[0])
        if value != 0:
            self.pc += self.get_value(params[1])
        else:
            self.pc += 1

    def op_tgl(self, *params):
        addr = self.pc + self.get_value(params[0])
        if addr >= len(self.memory.code):
            print(f">> tgl target {addr} out of bounds")
            self.pc += 1
            return
        target = self.memory.code[addr].split()
        print(self.pc, addr, "-->", " ".join(target))
        instr = target[0]
        if instr == "inc":
            target[0] = "dec"
        elif instr in ["dec", "tgl"]:
            target[0] = "inc"
        elif instr == "jnz":
            target[0] = "cpy"
        elif instr in ["cpy"]:
            target[0] = "jnz"

        self.memory.code[addr] = " ".join(target)
        print(">>>", " ".join(target))
        input("...")
        self.pc += 1

    def execute_next(self):
        nextline = self.memory.get_instruction(self.pc)
        if self.is_breakpoint(nextline):
            print(f"{self.pc:<4} {nextline}  {self.regs}")
            input("...")
        instr = nextline.split()
        self.get_operation(instr[0])(*instr[1:])

    def run(self):
        i = 0
        while self.pc < len(self.memory.code):
            i += 1
            self.execute_next()
            if i % 100000 == 0:
                print(i, self.regs)
            # input(">>")


def test_program_dec12():
    return  Memory([
        "cpy 41 a",
        "inc a",
        "inc a",
        "dec a",
        "jnz a 2",
        "dec a"
    ])


def program_dec12():
    return Memory([
        "cpy 1 a",
        "cpy 1 b",
        "cpy 26 d",
        "jnz c 2",
        "jnz 1 5",
        "cpy 7 c",
        "inc d",
        "dec c",
        "jnz c -2",
        "cpy a c",
        "inc a",
        "dec b",
        "jnz b -2",
        "cpy c b",
        "dec d",
        "jnz d -6",
        "cpy 17 c",
        "cpy 18 d",
        "inc a",
        "dec d",
        "jnz d -2",
        "dec c",
        "jnz c -5",
    ])


def test_program_dec23():
    return Memory([
        "cpy 2 a",
        "tgl a",
        "tgl a",
        "tgl a",
        "cpy 1 a",
        "dec a",
        "dec a",
    ])


def program_dec23():
    return Memory([
        "cpy a b",
        "dec b",
        "cpy a d",
        "cpy 0 a",
        "cpy b c",
        "inc a",
        "dec c",
        "jnz c -2",
        "dec d",
        "jnz d -5",
        "dec b",
        "cpy b c",
        "cpy c d",
        "dec d",
        "inc c",
        "jnz d -2",
        "tgl c",
        "cpy -16 c",
        "jnz 1 c",
        "cpy 75 c",
        "jnz 85 d",
        "inc a",
        "inc d",
        "jnz d -2",
        "inc c",
        "jnz c -5",
    ])


memory = program_dec23()
# memory = Memory(["tgl 1", "foo bar"])
cpu = Cpu(memory)
cpu.add_breakpoint(21)
cpu.add_breakpoint(18)
cpu.add_breakpoint("tgl c")
cpu.run()
print(cpu.regs)