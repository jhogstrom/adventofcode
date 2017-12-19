from collections import defaultdict

inp = [l.strip().split(" ") for l in open('18.txt')]
print(inp)

#snd X plays a sound with a frequency equal to the value of X.
#set X Y sets register X to the value of Y.
#add X Y increases register X by the value of Y.
#mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
#mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
#rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
#jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

class prg:
    def value(self, v):
        if v in self.regs:
            return self.regs[v]
        return int(v)

    def runinstr(self, instr):
        op = instr[0]
        print(op, instr, self.regs)
        if op == "snd":
            self.sound = self.value(instr[1])
        elif op == "set":
            self.regs[instr[1]] = self.value(instr[2])
        elif op == "add":
            self.regs[instr[1]] += self.value(instr[2])
        elif op == "mul":
            self.regs[instr[1]] *= self.value(instr[2])
        elif op == "mod":
            self.regs[instr[1]] %= self.value(instr[2])
        elif op == "rcv":
            if self.value(instr[1]) != 0:
                print("sound", self.sound, self.value(instr[1]))
                self.running = False
        elif op == "jgz":
            if self.value(instr[1]) > 0:
                #            print(pp, pp + value(instr[2]))
                self.pp += self.value(instr[2])
                return
        else:
            print("Unknown instruction:", op)
            exit(1)
        self.pp += 1

    def __init__(self):
        self.regs = defaultdict(int)
        self.pp = 0
        self.sound = 0
        self.running = True

p0 = prg()
p1 = prg()
p1.regs["p"] = 1

while p1.running:
    instr = inp[p1.pp]
    p1.runinstr(instr)

print("sound: ", p1.sound)
print(3423)


