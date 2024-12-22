import logging
from collections import defaultdict
from typing import List  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "17"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


class Computer:
    def __init__(self, A: int, B: int, C: int, pgm: List[int], debug: bool = False):
        self.reg = {"A": A, "B": B, "C": C}
        self.pc = 0
        self.terminated = False
        self.pgm = pgm
        self.output = []
        self.debug = debug

        self.opcodes = {
            0: "adv",
            1: "bxl",
            2: "bst",
            3: "jnz",
            4: "bxc",
            5: "out",
            6: "bdv",
            7: "cdv",
        }

    def run(self):
        while self.pc < len(self.pgm):
            if self.debug:
                print(self.pc, self.opcodes[self.pgm[self.pc]], self.reg)
            self.execute()
        if self.debug:
            print(self.pc, self.reg)
            print("Output:", ",".join(str(_) for _ in self.output))

    def dereference(self, addr: int) -> int:
        match self.pgm[addr]:
            case 0 | 1 | 2 | 3:
                return self.pgm[addr]
            case 4:
                return self.reg["A"]
            case 5:
                return self.reg["B"]
            case 6:
                return self.reg["C"]
            case _:
                raise ValueError(f"Unknown address mode {self.pgm[addr]}")

    def execute(self):
        match self.pgm[self.pc]:
            case 0:  # adv
                self.reg["A"] = self.reg["A"] // (2 ** self.dereference(self.pc + 1))
                self.pc += 2
            case 1:  # bxl
                self.reg["B"] = self.reg["B"] ^ self.pgm[self.pc + 1]
                self.pc += 2
            case 2:  # bst
                self.reg["B"] = self.dereference(self.pc + 1) % 8
                self.pc += 2
            case 3:  # jnz
                if self.reg["A"]:
                    self.pc = self.pgm[self.pc + 1]
                else:
                    self.pc += 2
            case 4:  # bxc
                self.reg["B"] = self.reg["B"] ^ self.reg["C"]
                self.pc += 2
            case 5:  # out
                self.output.append(self.dereference(self.pc + 1) % 8)
                self.pc += 2
            case 6:  # bdv
                self.reg["B"] = self.reg["A"] // (2 ** self.dereference(self.pc + 1))
                self.pc += 2
            case 7:  # cdv
                self.reg["C"] = self.reg["A"] // (2 ** self.dereference(self.pc + 1))
                self.pc += 2
            case _:
                raise ValueError(f"Unknown opcode {self.pgm[self.pc]}")


def parse_data(data):
    regs = defaultdict(int)
    pgm = []
    for line in data:
        if line.startswith("Register"):
            regs[line.split()[1][0]] = int(line.split(":")[1])
        if line.startswith("Program"):
            pgm = [int(_) for _ in line.split(":")[1].split(",")]

    return regs, pgm


@timeit
def star1(data):
    logging.debug("running star 1")
    regs, pgm = parse_data(data)
    # print(regs, pgm)
    c = Computer(**regs, pgm=pgm)
    c.run()
    print(f"Output: {', '.join(str(_) for _ in c.output)}")


def dec_to_octal(n):
    result = [0] * len(str(n) * 2)
    i = 0
    while n != 0:
        result[i] = n % 8
        n = int(n / 8)
        i += 1

    return "".join(str(_) for _ in result[:i][::-1])


def find_solution(known, pgm, regs):
    if len(known) == 16:
        return int(known, 8)

    valid = []
    for i in range(8):
        full = known + str(i) + "0" * (16 - len(known) - 1)
        a = int(full, 8)
        regs["A"] = a
        c = Computer(**regs, pgm=pgm, debug=False)
        c.run()
        if c.output[::-1][: len(known) + 1] == pgm[::-1][: len(known) + 1]:
            # print(f"VALID: {known:<16} {dec_to_octal(a)} {a} \n\t{c.output}\n\t{pgm}")
            valid.append(i)
    for v in valid:
        res = find_solution(known + str(v), pgm, regs)
        if res:
            return res


@timeit
def star2(data):
    logging.debug("running star 2")
    regs, pgm = parse_data(data)
    result = find_solution("", pgm, regs)
    print(f"Value of A: {result}")


star1(data)
star2(data2)
