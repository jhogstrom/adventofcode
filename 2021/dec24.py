import os
from typing import List
from timer import timeit
from collections import defaultdict, deque

stardate = 24
dataname = f"dec{stardate}.txt"
dataname = f"dec{stardate}_test.txt"
dataname = f"dec{stardate}_ex3.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Computer():
    def __init__(self, input_buffer) -> None:
        regs = "xyzw"
        self.input_buffer = input_buffer
        self.input_ptr = 0

        self.regs = {reg: 0 for reg in regs}

    def __str__(self) -> str:
        return str(self.regs)

    def inp(self, a):
        self.regs[a] = int(self.input_buffer[self.input_ptr])
        self.input_ptr += 1

    def add(self, a, b):
        b = self.regs[b] if b in self.regs else int(b)
        self.regs[a] += b

    def mul(self, a, b):
        b = self.regs[b] if b in self.regs else int(b)
        self.regs[a] *= b

    def div(self, a, b):
        b = self.regs[b] if b in self.regs else int(b)
        self.regs[a] /= b
        self.regs[a] = int(self.regs[a])

    def mod(self, a, b):
        b = self.regs[b] if b in self.regs else int(b)
        self.regs[a] %= b

    def eql(self, a, b):
        b = self.regs[b] if b in self.regs else int(b)
        self.regs[a] = 1 if self.regs[a] == b else 0

    def runinstruction(self, instruction, *args):
        ins = getattr(self, instruction)
        ins(*args)

    def process(self, instruction):
        tokens = instruction.split()
        self.runinstruction(tokens[0], *tokens[1:])
        # print(f"{instruction} => {self}")


class Program():
    def __init__(self, code, input) -> None:
        self.code = code
        self.computer = Computer(input)

    def run(self):
        for i in (_ for _ in self.code if not _.startswith("#")):
            if i == "":
                return
            self.computer.process(i)

    def __str__(self) -> str:
        return str(self.computer)

class Monad():
    def __init__(self, code, input) -> None:
        self.input = input
        self.program = Program(code, list(input))

    def run(self):
        # if "0" in self.input:
        #     return False
        self.program.run()
        return self.program.computer.regs['z'] == 0

    def __str__(self) -> str:
        return str(self.program)

class PyProgr():
    def __init__(self, input_buffer) -> None:
        self.regs = {reg: 0 for reg in "xyzw"}
        self.input_buffer = input_buffer
        self.input_ptr = 0
        self.x = self.y = self.z = self.w = 0

    def take_input(self):
        self.input_ptr += 1
        return int(self.input[self.input_ptr-1])

    def run(self):
        # block 1:
        #     # inp w
        self.w = self.take_input
        #     # mul x 0
        #     # add x z
        #     # mod x 26
        #     # div z 1
        #     # add x 14
        # self.x = 14
        #     # eql x w
        #     # eql x 0
        self.x = int((self.z % 26) + 14 != self.w)

        # self.x = 1
        #     # mul y 0
        #     # add y 25
        #     # mul y x
        #     # add y 1
        # self.y = 26
        #     # mul z y
        self.z *= self.x * 25 + 1
        #     # mul y 0
        #     # add y w
        #     # add y 8
        #     # mul y x
        #     # self.y = self.w + 8
        #     # add z y
        # self.z = self.w + 8
        self.z += (self.w + 8) * self.x


        self.z = self.take_input() + 8

        # block 2
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # self.x = self.z % 26
            # div z 1
            # add x 15
            # self.x = (self.z % 26) + 15
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 15 != self.w)
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= self.x * 25 + 1
            # mul y 0
            # add y w
            # add y 11
        # self.y = self.w + 11
            # mul y x
        # self.y = (self.w + 11) * self.x
            # add z y
        self.z += (self.w + 11) * self.x

            # # Block3
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 1
            # add x 13
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 13 != self.w)
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 2
            # mul y x
        # self.y = (self.w + 2) * self.x
            # add z y
        self.z +=(self.w + 2) * self.x

            # # Block4
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -10
            # self.x = (self.z % 26) - 10
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) - 10 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 11
            # mul y x
        # self.y = (self.w + 11) * self.x
            # add z y
        self.z += (self.w + 11) * self.x

        # block5
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 1
            # add x 14
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 14 != self.w)
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 1
            # mul y x
        # self.y = (self.w + 1) * self.x
            # add z y
        self.z += (self.w + 1) * self.x

            # block 6
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -3
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) - 3 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 5
            # mul y x
            # add z y
        self.z += (self.w + 5) * self.x

            # Block 7
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -14
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) - 14 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 10
            # mul y x
            # add z y
        self.z += (self.w + 10) * self.x

            # block 8
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 1
            # add x 12
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 12 != self.w)
        # self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 6
            # mul y x
            # add z y
        self.z += (self.w + 6) * self.x

            # block 9
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 1
            # add x 14
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 14 != self.w)
        # self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 1
            # mul y x
            # add z y
        self.z += (self.w + 1) * self.x

            # block10
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 1
            # add x 12
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) + 12 != self.w)
        # self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 11
            # mul y x
            # add z y
        self.z += (self.w + 11) * self.x

            # Block 11
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -6
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) -6 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 9
            # mul y x
            # add z y
        self.z += (self.w + 9) * self.x

            # Block 12
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -6
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) -6 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 14
            # mul y x
            # add z y
        self.z += (self.w + 14) * self.x

            # block 13
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -2
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) - 2 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 11
            # mul y x
            # add z y
        self.z += (self.w + 11) * self.x

            # block 14
            # inp w
        self.w = self.take_input()
            # mul x 0
            # add x z
            # mod x 26
            # div z 26
            # add x -9
            # eql x w
            # eql x 0
        self.x = int((self.z % 26) - 9 != self.w)
        self.z = self.z // 26
            # mul y 0
            # add y 25
            # mul y x
            # add y 1
            # mul z y
        self.z *= (25 * self.x) + 1
            # mul y 0
            # add y w
            # add y 2
            # mul y x
            # add z y
        self.z += (self.w + 2) * self.x

    def run(self):
        # block 1:
        self.w = self.take_input
        self.x = int((self.z % 26) + 14 != self.w)
        self.z *= self.x * 25 + 1
        self.z += (self.w + 8) * self.x

        # block 2
        self.w = self.take_input()
        self.x = int((self.z % 26) + 15 != self.w)
        self.z *= self.x * 25 + 1
        self.z += (self.w + 11) * self.x

        # Block3
        self.w = self.take_input()
        self.x = int((self.z % 26) + 13 != self.w)
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 2) * self.x

        # Block4
        self.w = self.take_input()
        self.x = int((self.z % 26) - 10 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 11) * self.x

        # block5
        self.w = self.take_input()
        self.x = int((self.z % 26) + 14 != self.w)
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 1) * self.x

        # block 6
        self.w = self.take_input()
        self.x = int((self.z % 26) - 3 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 5) * self.x

        # Block 7
        self.w = self.take_input()
        self.x = int((self.z % 26) - 14 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 10) * self.x

        # block 8
        self.w = self.take_input()
        self.x = int((self.z % 26) + 12 != self.w)
        # self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 6) * self.x

        # block 9
        self.w = self.take_input()
        self.x = int((self.z % 26) + 14 != self.w)
        # self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 1) * self.x

        # block10
        self.w = self.take_input()
        self.x = int((self.z % 26) + 12 != self.w)
        # self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 11) * self.x

        # Block 11
        self.w = self.take_input()
        self.x = int((self.z % 26) -6 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 9) * self.x

        # Block 12
        self.w = self.take_input()
        self.x = int((self.z % 26) -6 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 14) * self.x

        # block 13
        self.w = self.take_input()
        self.x = int((self.z % 26) - 2 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 11) * self.x

        # block 14
        self.w = self.take_input()
        self.x = int((self.z % 26) - 9 != self.w)
        self.z = self.z // 26
        self.z *= (25 * self.x) + 1
        self.z += (self.w + 2) * self.x


class PyMonad():
    def __init__(self, digit: int) -> None:
        self.digit = digit
        self.monad = getattr(self, f"d{digit}")
        # self.monads = {_: getattr(self, f"d{_}") for _ in range(1, 3)}

    def d1(self, w: int, z: int) -> int:
        x = int((z % 26) + 14 != w)
        z *= x * 25 + 1
        z += (w + 8) * x
        return z

    def d2(self, w, z) -> int:
        x = int((z % 26) + 15 != w)
        z *= x * 25 + 1
        z += (w + 11) * x
        return z

    def d3(self, w, z) -> int:
        x = int((z % 26) + 13 != w)
        z *= (25 * x) + 1
        z += (w + 2) * x
        return z

    def d4(self, w, z) -> int:
        x = int((z % 26) - 10 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 11) * x
        return z

    def d5(self, w, z) -> int:
        x = int((z % 26) + 14 != w)
        z *= (25 * x) + 1
        z += (w + 1) * x
        return z

    def d6(self, w, z) -> int:
        x = int((z % 26) - 3 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 5) * x
        return z

    def d7(self, w, z) -> int:
        # Block 7
        x = int((z % 26) - 14 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 10) * x
        return z

    def d8(self, w, z) -> int:
        # block 8
        x = int((z % 26) + 12 != w)
        # z = z // 26
        z *= (25 * x) + 1
        z += (w + 6) * x
        return z

    def d9(self, w, z) -> int:
        # block 9
        x = int((z % 26) + 14 != w)
        # z = z // 26
        z *= (25 * x) + 1
        z += (w + 1) * x
        return z

    def d10(self, w, z) -> int:
        # block10
        x = int((z % 26) + 12 != w)
        # z = z // 26
        z *= (25 * x) + 1
        z += (w + 11) * x
        return z

    def d11(self, w, z) -> int:
        # Block 11
        x = int((z % 26) -6 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 9) * x
        return z

    def d12(self, w, z) -> int:
        # Block 12
        x = int((z % 26) -6 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 14) * x
        return z

    def d13(self, w, z) -> int:
        # block 13
        x = int((z % 26) - 2 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 11) * x
        return z

    def d14(self, w, z) -> int:
        # block 14
        x = int((z % 26) - 9 != w)
        z = z // 26
        z *= (25 * x) + 1
        z += (w + 2) * x
        return z


    def run(self, inp, z) -> int:
        return self.monad(inp, z)


class MyMonad():
    def __init__(self, digit: int) -> None:
        dataname = f"dec24_m{digit}.txt"
        curdir = os.path.dirname(os.path.abspath(__file__))
        filename = f'{curdir}\\{dataname}'
        self.program = [_.strip() for _ in open(filename, 'r').readlines()]

    def run(self, input, zreg):
        computer = Computer([input])
        computer.regs['z'] = zreg
        for c in self.program:
            computer.process(c)
        return computer.regs['z']

def find_z(block: int, targets: List[int], zrange) -> List[int]:
    res = []
    valid_digits = set()
    for i in range(1, 10):
        for z in zrange:
            m = MyMonad(14)
            zout = m.run(i, z)
            if zout in targets:
                # print(block, i, z, zout)
                valid_digits.add(i)
                res.append(z)
    return res, valid_digits

def get_z(inp, z_values_map, valid_output):
    print("Monad #", inp)
    z_output = set()
    monad = PyMonad(inp)
    res = defaultdict(list)
    # for i in range(9, 0, -1):
    for i in range(1, 10):
        print("running on input", i)
        for z_list in z_values_map.values():
            for z in z_list:
                output = monad.run(i, z)
                if not output in z_output:
                    if inp in valid_output:
                        if output not in valid_output[inp]:
                            continue
                        print("Valid (i, z, result)", i, z, output)
                        exit()
                    z_output.add(output)
                    res[i].append(output)
        # print(f"  {i}: {len(res[i])} - Total unique: {len(z_output)}")
    # print("Unique z", len(z_output))
    return res

import json

@timeit
def star1(data):
    z_values = {1: {0: [0]}}
    valid_output1 = {
        1: [17], # 9
        2: [462], # 9
        3: [12023], # 9
        4: [462], # 1
        5: [12022], # 9
        6: [462], # 7
        7: [17], # 6
        8: [453], # 5
        9: [11788], # 9
        10: [306503], # 4
        11: [11788], # 9
        12: [453], # 4
        13: [17],  # 9
        14: [0],  # 8
    }
    valid_output = {
        1: [10], # 2
        2: [275], # 4
        3: [7161], # 9
        4: [275], # 1
        5: [7154], # 3
        6: [275], # 1
        7: [10], # 1
        8: [267], # 1
        9: [6949], # 6
        10: [180686], # 1
        11: [6949], # 6
        12: [267], # 1
        13: [10], # 5
        14: [0], # 1
    }
    for inp in range(1, 15):
        z_values[inp+1] = get_z(inp, z_values[inp], valid_output)
        print(inp)
        # print(z_values)

    return

@timeit
def star2(data):
    ...

data2 = data[:]
star1(data)
star2(data2)

#99998231440000