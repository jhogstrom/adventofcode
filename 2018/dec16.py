from collections import defaultdict
all=[_.strip() for _ in open("16_1",'r').readlines()]

debug = False
def debugprint(s):
	if debug:
		print(s)

def getregA(regs, indata):
	s = "getregA({0})=>{1} Regs: {2}  Indata: {3}".format(getvalA(regs, indata),\
		regs[indata[1]],\
		regs, indata)
	debugprint(s)
	return regs[indata[1]]
def getregB(regs, indata):
	s = "getregB({0})=>{1} Regs: {2}  Indata: {3}".format(getvalB(regs, indata),\
		regs[indata[2]],\
		regs, indata)
	debugprint(s)
	return regs[indata[2]]
def getvalA(regs, indata):
	#print(indata)
	return indata[1]
def getvalB(regs, indata):
	#print(indata)
	return indata[2]

def add(a, b):
	debugprint("add({0}, {1})". format(a, b))
	return a + b

def mul(a, b):
	debugprint("mul({0}, {1})". format(a, b))
	return a * b

def bitwiseand(a, b):
	debugprint("bitwiseand({0}, {1})". format(a, b))
	return a & b

def bitwiseor(a, b):
	debugprint("bitwiseor({0}, {1})". format(a, b))
	return a | b

def assign(a, b):
	debugprint("assign({0}, {1})". format(a, b))
	return a

def greaterthan(a, b):
	debugprint("greaterthan({0}, {1})". format(a, b))
	if a > b:
		return 1
	return 0
def equality(a, b):
	debugprint("equality({0}, {1})". format(a, b))
	if a == b:
		return 1
	return 0


ops = dict()
ops['addr'] = [getregA, getregB, add]
ops['addi'] = [getregA, getvalB, add]

ops['mulr'] = [getregA, getregB, mul]
ops['muli'] = [getregA, getvalB, mul]

ops['banr'] = [getregA, getregB, bitwiseand]
ops['bani'] = [getregA, getvalB, bitwiseand]

ops['borr'] = [getregA, getregB, bitwiseor]
ops['bori'] = [getregA, getvalB, bitwiseor]

ops['setr'] = [getregA, getvalB, assign]
ops['seti'] = [getvalA, getvalB, assign]

ops['gtir'] = [getvalA, getregB, greaterthan]
ops['gtri'] = [getregA, getvalB, greaterthan]
ops['gtrr'] = [getregA, getregB, greaterthan]

ops['eqir'] = [getvalA, getregB, equality]
ops['eqri'] = [getregA, getvalB, equality]
ops['eqrr'] = [getregA, getregB, equality]

def execute(op, regs, indata):
	r = op[2](op[0](regs, indata), op[1](regs, indata))
	regc = indata[3]
	res = regs[:regc] + [r] + regs[regc+1:]
#	res = regs[0:2] + [r] + regs[-1:]
	r = ""
	for c in res:
		r += str(c)
	return r

def readinstructions():
	instructions = []
	for i in range(1 + len(all)//4):
		regs = [int(_) for _ in all[i*4].split("[")[1][:-1].split(",")]
		indata = [int(_) for _ in all[i*4 + 1].split()]
		after = [_.strip() for _ in all[i*4 + 2].split("[")[1][:-1].split(",")]

		r = ""
		for c in after:
			r += c
		instructions.append([regs, indata, r])
	return instructions

def executeops(instruction):
	res = 0
	for o in ops.keys():
		opres = execute(ops[o], instruction[0], instruction[1])
		if opres == instruction[2]:
#			print("{0} <= {1}, {2} => {3} ({4})".format(o, instruction[0], i[1], opres, i[2]))
			res += 1
	return res

def countmultisolutions(instructions):
	totalcorrect = 0
	for i in instructions:
		if executeops(i) >= 3:
			totalcorrect += 1

	print("Matching three or more:", totalcorrect, len(instructions))

def executeopsandmap(instruction):
	mapped = defaultdict(list)
	for opname in ops.keys():
		opres = execute(ops[opname], instruction[0], instruction[1])
		
		if opres == instruction[2]:
			opcode = instruction[1][0]
			mapped[opcode].append(opname)
	return mapped

def findallsame(k, alist):
	if len(alist) == 1: return
	allsame = True
	for o in alist:
		if o != alist[0]:
			allsame = False
			break
	if allsame:
		print("=>", k, alist[0])
		return alist[0]
	return None

def findunique(correctop):
	for m in sorted(correctop.keys()):
		unique = findallsame(m, correctop[m])
		if unique != None:
			return unique
	return None

def removeunique(u, correctop):
	for m in sorted(correctop.keys()):
		while u in correctop[m]:
			correctop[m].remove(u)
		if correctop[m] == []: correctop[m] = [u]

def mapinstructions(instructions):
	correctop = defaultdict(list)
	for i in instructions:
		mapped = executeopsandmap(i)
		for m in mapped.keys():
			correctop[m] += mapped[m]

	for i in range(len(ops)):
		u = findunique(correctop)
		removeunique(u, correctop)

	res = dict()
	for m in sorted(correctop.keys()):
		res[m] = correctop[m][0]

	return res


instructions = readinstructions()
countmultisolutions(instructions)
opmap = mapinstructions(instructions)
print(opmap)

class Computer:
	def __init__(self, opmap):
		self.regs = [0, 0, 0, 0]
		self.opmap = opmap
	def execute(self, instr):
		instr = [int(_) for _ in instr]
		operation = self.opmap[instr[0]]
		op = ops[operation]

		r = op[2](op[0](self.regs, instr), op[1](self.regs, instr))
		regc = instr[3]
		self.regs[regc] = r

	def printregs(self):
		print(self.regs)


program = [_.strip().split() for _ in open("16_2",'r').readlines()]

c = Computer(opmap)
for p in program:
	c.execute(p)
c.printregs()