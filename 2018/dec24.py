from collections import defaultdict

class Unit:
	def __init__(self):
		self.count = 0
		self.hitpoints = 0
		self.weakness = []
		self.immunity = []
		self.attack = ""
		self.attackdamage = 0
		self.initiative = 0
		self.isimmune = True
		self.groupnum = 0
		

	def __str__(self):
		_str = "{0}#{1:2}: {2:5} ({3:4}*{4:4}). ".format(self.astype()[1:], self.groupnum, self.effectivepower(),
			self.count, self.attackdamage)
		_str += "Attack: {0}/{1} Ini {2}. ".format(self.attack, self.hitpoints, self.initiative)
		if len(self.immunity) > 0:
			_str += "Immune to " + ", ".join(self.immunity)
			_str += ";"
		if len(self.weakness) > 0:
			_str += "Weak to " + ", ".join(self.weakness)
		return _str

	def __lt__(self, other):
		if self.effectivepower() == other.effectivepower():
			return self.initiative < other.initiative
		return self.effectivepower() < other.effectivepower()

	def astype(self):
		if self.isimmune: return "0Immune"
		return "1Infect"

	def effectivepower(self):
		return self.count * self.attackdamage

	def isalive(self):
		return self.count > 0

	def damageby(self, other):
		res = other.effectivepower()
		if other.attack in self.immunity: res = 0
		elif other.attack in self.weakness: res *= 2
		return res

	def attackedby(self, other):
		damage = self.damageby(other)
		unitslost = damage // self.hitpoints
#		print("{0}#{1} attacks {2}#{3} killing {4} units ({5}//{6})".format(\
#			other.astype(), other.groupnum, self.astype()[1:], self.groupnum, min(unitslost, self.count), damage, self.hitpoints)) 
		self.count -= unitslost
#		if not self.isalive():
#			print("==> {0}#{1} died!".format(self.astype()[1:], self.groupnum))



class Immunesystem:
	def __init__(self, filename):
		self.fightcount = 0
		self.units = []
		self.readunits(filename)

#		self.sampledata()

	def sampledata(self):
		u = Unit()
		u.initiative = 1000
		u.count = 1
		u.hitpoints = 2
		u2 = Unit()
		u2.initiative = 100
		u2.count = 1
		u2.hitpoints = 3
		self.units = [u, u2]

	def readunits(self, filename):
		all=[_.strip() for _ in open(filename,'r').readlines()]
		isImmune = True
		for l in all:
			if l == "Immune System:":
				isImmune = True
				continue
			if l == "Infection:":
				isImmune = False
				continue
			if l == "": continue
			w = l.split()
		#	print(w)
			u = Unit()
			u.count = int(w[0])
			u.isimmune = isImmune
			u.hitpoints = int(w[4])
			u.initiative = int(w[-1])
			u.attack = w[-5]
			u.attackdamage = int(w[-6])
			if "(" in l:
				s = [_.strip() for _ in l[l.index("(")+1:l.index(")")].replace(",", "").split(";")]
				for x in s:
					w = x.split()
					if w[0] == "weak":
						u.weakness = w[2:]
					else:
						u.immunity = w[2:]
			self.units.append(u)
			u.groupnum = len([_ for _ in self.units if _.isimmune == u.isimmune])
			#print(u)
	def fight(self):
		self.fightcount += 1
		print("Fight {0}: {1}/{2}".format(self.fightcount, self.immunecount(), self.infectcount()))
		#immunesystem.printunits(immunesystem.liveunits(), "FIGHT {0}".format(self.fightcount))

		self.targetselection()
		self.attack()

	def printunits(self, units, title=""):
		print("={0}vv".format(title))
		for u in units:
			print(u)
		print("=^^")


	def makeselection(self, groups):
		for u in groups:
			enemies = [_ for _ in self.enemies(u) if not _ in self.selected and _.damageby(u) > 0]
			enemies = sorted(enemies, reverse=True, key=lambda x: (x.damageby(u), x.effectivepower(), x.initiative))
			if len(enemies) > 0:
				self.selected.append(enemies[0])
				self.fights[u] = enemies[0]

	def targetselection(self):
		self.selected = []
		self.fights = dict()
		groups = sorted(self.liveunits(), reverse=True, key=lambda x: (x.effectivepower(), x.initiative))
		self.makeselection(groups)


	def attack(self):
		for f in sorted(self.fights, reverse=True, key=lambda x: x.initiative):
			if f.isalive():
				self.fights[f].attackedby(f)

	def liveunits(self):
		return [_ for _ in self.units if _.isalive()]


	def enemies(self, unit):
		return [_ for _ in self.liveunits() if _.isimmune != unit.isimmune]

	def infectiongroups(self):
		return [_ for _ in self.liveunits() if not _.isimmune]

	def immunegroups(self):
		return [_ for _ in self.liveunits() if _.isimmune]

	def immunecount(self):
		return sum([_.count for _ in self.immunegroups()])

	def infectcount(self):
		return sum([_.count for _ in self.infectiongroups()])

	def boostimmune(self, boost):
		for _ in self.immunegroups():
			_.attackdamage += boost




filename = "24"
boost = 34
immunewon = False
booststep = 1
immuneresult = 0
infectresult = 0
while booststep >= 1:
	while not immunewon:
		boost += booststep
		print("Boosting", boost)
		immunesystem = Immunesystem(filename)
		immunesystem.boostimmune(boost)
		while len(immunesystem.infectiongroups()) > 0 and len(immunesystem.immunegroups()) > 0:
			immunesystem.fight()

		immuneresult = sum([_.count for _ in immunesystem.immunegroups()])
		infectresult = sum([_.count for _ in immunesystem.infectiongroups()])
		immunewon = immuneresult > 0

	print("Immune won with boost {0}. Restarting at {1} step {2}".format(boost, boost-booststep, booststep // 10))
	if booststep == 1:
		break
	boost -= booststep
	booststep = booststep // 10
	immunewon = False

print("Final result")
print("Boost:", boost)
print("Immune count:", immuneresult)
print("infect count:", infectresult)

exit()
for _ in immunesystem.immunegroups():
	print(_)

print("===")

for _ in immunesystem.infectiongroups():
	print(_)



#Less than: 20411, 20415