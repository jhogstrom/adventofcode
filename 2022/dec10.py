data = open(0).read().splitlines()

PIX_WIDTH = 3


class Cpu():
    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self.cycle = self.total_strength = 0
        self.x = 1
        self.monitor = []
        for row in range(6):
            self.monitor.append([" " * PIX_WIDTH for _ in range(40)])

    @property
    def row(self):
        return self.cycle // 40

    def debug(self, s):
        if self._debug:
            print(s)

    def inc_cycle(self):
        hpos = self.cycle % 40
        if hpos in [self.x-1, self.x, self.x+1]:
            self.monitor[self.row][hpos] = "#" * PIX_WIDTH

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
        self.x += int(args[0])

    def exec(self, op: str):
        if op == "noop":
            return self.noop
        if op == "addx":
            return self.addx
        raise ValueError(f"No such op: {op}")

    def execute(self, instr):
        instr = instr.split()
        self.exec(instr[0])(*instr[1:])
        self.debug(f"({self.cycle}) - {instr[0]}({','.join(instr[1:])}) :: {self.x}")


cpu = Cpu()
[cpu.execute(_) for _ in data]

print("star1:", cpu.total_strength)
for r in range(6):
    print("star2: ", "".join(cpu.monitor[r]))

# Powershell: Get-Content dec10.txt | python .\dec10.py
# cmd: python dec10.py < dec10.txt
