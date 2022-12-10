import os

runtest = False
stardate = "10"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Cpu():
    def __init__(self, code, debug: bool = False) -> None:
        self.code = code
        self.cycle = 0
        self.pc = 0
        self.x = 1
        self.total_strength = 0
        self.monitor = []
        self._debug = debug
        for row in range(6):
            self.monitor.append([" " for _ in range(40)])

    @property
    def row(self):
        return self.cycle // 40

    def debug(self, s):
        if self._debug:
            print(s)

    def inc_cycle(self):
        hpos = self.cycle % 40
        if hpos in [self.x-1, self.x, self.x+1]:
            self.monitor[self.row][hpos] = "#"

        self.cycle += 1
        if (self.cycle - 20) % 40 == 0:
            signal = self.x * self.cycle
            self.total_strength += signal
            self.debug(f"cycle: {self.cycle} Strength: {self.x} signal: {signal}  ==== {self.total_strength}")

    def noop(self, *args):
        self.inc_cycle()

    def addx(self, *args):
        self.inc_cycle()
        self.inc_cycle()
        v = int(args[0])
        self.x += v

    def exec(self, op: str):
        if op == "noop":
            return self.noop
        if op == "addx":
            return self.addx
        raise ValueError(f"No such op: {op}")

    def execute(self):
        instr = self.code[self.pc].split()
        self.exec(instr[0])(*instr[1:])
        self.pc += 1
        self.debug(f"{self.pc}({self.cycle}) - {instr[0]}({','.join(instr[1:])}) :: {self.x}")


def star1():
    cpu = Cpu(data)
    while cpu.pc < len(data):
        cpu.execute()
    return cpu.total_strength


def star2():
    cpu = Cpu(data)
    while cpu.pc < len(data):
        cpu.execute()
    for r in range(6):
        print("".join(cpu.monitor[r]))


print("star1:", star1())
print("star2")
star2()
