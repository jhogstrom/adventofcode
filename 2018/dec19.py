from collections import defaultdict
all=[_.strip() for _ in open("19",'r').readlines()]

debug = False
def debugprint(s):
	if debug:
		print(s)

def getregA(regs, indata):
	s = "getregA({0})=>{1} Regs: {2}  Indata: {3}".format(getvalA(regs, indata),\
		regs[indata[0]],\
		regs, indata)
	debugprint(s)
	return regs[indata[0]]
def getregB(regs, indata):
	s = "getregB({0})=>{1} Regs: {2}  Indata: {3}".format(getvalB(regs, indata),\
		regs[indata[1]],\
		regs, indata)
	debugprint(s)
	return regs[indata[1]]
def getvalA(regs, indata):
	#print(indata)
	return indata[0]
def getvalB(regs, indata):
	#print(indata)
	return indata[1]

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

class Computer:
	def __init__(self):
		self.regs = [0, 0, 0, 0, 0, 0]
		self.ppreg = 0

	def pp(self):
		return self.regs[self.ppreg]

	def formatregs(self, lst):
		res = "["
		for r in lst:
			res += "{0:4},".format(r)
#			print(">{0}<  <{1}>".format(res, r))
		res = res[:-1] + "]"
#		print(res)
#		exit()
		return res


	def run(self, program):
		instr = program[0]
		self.ppreg = int(instr.split()[1])
		program.remove(instr)
		i = 0
		while self.pp() in range(len(program)):
			instr = program[self.pp()]
			pp = self.pp()
			regs = self.formatregs(self.regs)
			self.executeop(instr.split())
			i += 1
			print("{4:6} ip {0:3} {1} {2} {3}".format(pp, \
				regs, instr.split()[0], self.formatregs(self.regs), i))
			if i == 30000:
				exit()
			self.regs[self.ppreg] += 1

		print("Completed")
		self.printregs()


	def executeop(self, instr):
		operation = instr[0]		
		instr = [int(_) for _ in instr[1:]]
		op = ops[operation]

		r = op[2](op[0](self.regs, instr), op[1](self.regs, instr))
		regc = instr[2]
		self.regs[regc] = r

	def printregs(self):
		print(self.regs)

c = Computer()
c.run(all)


