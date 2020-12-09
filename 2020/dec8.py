import os
import itertools
from timing import timeit
import logging

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

logging.basicConfig(level=logging.DEBUG)

# data = [
#     "nop +0",
# "acc +1",
# "jmp +4",
# "acc +3",
# "jmp -3",
# "acc -99",
# "acc +1",
# "jmp -4",
# "acc +6"
# ]

class IntComputer():
    def __init__(self, code, *, debug: bool = False):
        self.code = code
        self.debug = debug
        self.reset()

    def reset(self):
        self.p = 0
        self.executedlines = []
        self.acc = 0

    def log(self, s):
        if self.debug:
            print(s)

    def executeline(self, line):
        # self.log(f"{self.p:3} {line} - {self.acc}")

        # Been here before?
        if self.p in self.executedlines:
            return False
        self.executedlines.append(self.p)

        # execute instruction
        instr, param = line.split()
        if instr == "acc":
            self.acc += int(param)
            self.p += 1
        elif instr == "nop":
            self.p += 1
        elif instr == "jmp":
            self.p += int(param)

        # Execution successful
        return True

    def run(self):
        """
        Execute lines. Return True if executed to the end, False if stuck in a loop
        """
        while self.p < len(self.code):
            if not self.executeline(self.code[self.p]):
                return False
        return True

        self.log("done")

    def runmod(self):
        completed = False
        for i, line in enumerate(self.code):
            self.reset()
            if "jmp" in line:
                self.code[i] = line.replace("jmp", "nop")
                if self.run():
                    return
                self.code[i] = line
            elif "nop" in line:
                self.code[i] = line.replace("nop", "jmp")
                if self.run():
                    return
                self.code[i] = line
        raise Exception("That didn't go well...")



debug = False


@timeit
def star1():
    c = IntComputer(data, debug=debug)
    c.run()
    print(f"* {c.acc}")


@timeit
def star2():
    c = IntComputer(data, debug=debug)
    c.runmod()
    print(f"** {c.acc}")


star1()
star2()
