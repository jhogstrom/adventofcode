import os
import itertools
from timing import timeit

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec8.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

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
        self.log(f"{self.p:3} {line} - {self.acc}")
        # Been here before?
        if self.p in self.executedlines:
            self.log(self.acc)
            return False

        # Remember where we've been
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
        modified_jmp = []
        org_code = [_ for _ in self.code]
        count = 0
        completed = False
        while not completed:
            # restore code
            self.code = [_ for _ in org_code]
            self.reset()
            # replace one line
            for i, line in enumerate(self.code):
                if "jmp" in line and i not in modified_jmp:
                    self.code[i] = line.replace("jmp", "nop")
                    self.log(f"{i}: replaced {self.code[i]}")
                    modified_jmp.append(i)
                    break
            # run modified code
            completed = self.run()

            # Safety switch...
            count += 1
            if count > len(org_code):
                print("PROBLEM")
                return
        self.log(self.acc)


debug = False
def star1():
    c = IntComputer(data, debug=debug)
    c.run()
    print(f"* {c.acc}")

def star2():
    c = IntComputer(data, debug=debug)
    c.runmod()
    print(f"** {c.acc}")


star1()
star2()