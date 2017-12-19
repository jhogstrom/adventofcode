from collections import defaultdict

inp = [l.strip().split(" ") for l in open('18.txt')]

class prg:
    def value(self, v):
        if v in self.regs:
            return self.regs[v]
        return int(v)

    def receive(self, v):
        self.queue.append(v)

    def runinstr(self, instr, other):
        op = instr[0]
        if op == "snd":
            other.receive(self.value(instr[1]))
            self.sent += 1
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
            if len(self.queue) > 0:
                self.regs[instr[1]] = self.queue[0]
                self.queue = self.queue[1:]
                self.running = True
            else:
                self.running = False
                return
        elif op == "jgz":
            if self.value(instr[1]) > 0:
                self.pp += self.value(instr[2])
                return
        self.pp += 1

    def __init__(self):
        self.regs = defaultdict(int)
        self.pp = 0
        self.running = True
        self.queue = []
        self.sent = 0

p0 = prg()
p1 = prg()
p1.regs["p"] = 1

while 1:
    p0.runinstr(inp[p0.pp], p1)
    p1.runinstr(inp[p1.pp], p0)
    #print("{} [{}] / {} [{}] -- {}".format(p0.pp, p0.running, p1.pp, p1.running, p1.sent))
    if not (p0.running or p1.running):
        break

print(p1.sent)
print("should be 7493")


