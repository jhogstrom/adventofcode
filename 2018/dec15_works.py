from collections import defaultdict

class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __lt__(self, other):
		if self.y == other.y:
			return self.x < other.x
		return self.y < other.y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash(str(self))

	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def new(self, dx, dy):
		return Coordinate(self.x + dx, self.y + dy)

	def adjacentcells(self):
		return [self.new(1, 0), self.new(-1, 0), self.new(0, 1), self.new(0, -1)]


class Creature:
	def __init__(self, x, y, m, ctype, power):
		self.map = m
		self.coord = Coordinate(x, y)
		self.x = x
		self.y = y
		self.ctype = ctype
		self.attackpower = power
		self.health = 200
	def __lt__(self, other):
		return self.coord < other.coord
	def __str__(self):
		return "{0}({1})".format(self.coord, self.ctype)
	def alive(self):
		return self.health > 0

	def isadjacent(self, e):
		return e.onpos(self.coord.new(-1, 0)) or \
			e.onpos(self.coord.new(1, 0)) or \
			e.onpos(self.coord.new(0, -1)) or \
			e.onpos(self.coord.new(0, +1))

	def onpos(self, c):
		return self.coord == c

	def adjacentcells(self):
		res = self.coord.adjacentcells()
		#print(self.x, self.y, res)
		return [_ for _ in res if self.map.isfloor(_)]

	def gettargetpositions(self, enemies):
		res = []
		for e in enemies:
			res += e.adjacentcells()
		return [_ for _ in res if not self.map.isoccupied(_)]

	def getenemies(self):
		if self.ctype == "E":
			return self.map.goblins()
		return self.map.elves()

	def reachable(self, coord):
		for n in coord.adjacentcells():
			if self.map.isfloor(n) and not self.map.isoccupied(n) and (not n in self.seen):
				self.seen.append(n)
				self.reachable(n)

	def getreachable(self, coord):
		self.seen = []
		self.reachable(coord)
		return self.seen

	def printintermediate(self, arr, c):
		return
		g = self.map.getprintablegrid()
		for _ in arr:
			g[_.y][_.x] = c
		self.map.printgrid(grid=g)


	def floodfill(self, startcoord, reachabletargets):
		mapped = defaultdict()
		def fill(nodes, dist):
			edge = []
			for n in nodes:
				if (not n in mapped) or (mapped[n] > dist):
					mapped[n] = dist
					edge += [_ for _ in n.adjacentcells() if _ in reachabletargets]
			return edge

		newnodes = [_ for _ in startcoord.adjacentcells() if _ in reachabletargets]
		dist = 0
		while len(mapped) < len(reachabletargets):
			dist += 1
			newnodes = fill(newnodes, dist)
		mapped[startcoord] = 0
		return mapped

	def move(self):
		# Get list of alive enemies
		enemies = [_ for _ in self.getenemies() if _.alive()]

		# Check if we're already in attack position - then we shouldn't move.
		for e in enemies:
			if self.isadjacent(e):
#				print("{0} has enemy close ({1})".format(self, e))
				return

		# Check if we cannot move. If not, we shouldn't move
		c = self.adjacentcells()
		for _ in self.map.livingcreatures():
			if _.coord in c:
				c.remove(_.coord)
		if c == []:
			print("{0} has nowhere to move".format(self))
			return

		# Get the targetpositions
		targetpositions = self.gettargetpositions(enemies)
		self.printintermediate(targetpositions, "?")

		# Get all reachable cells
		allreachable = self.getreachable(self.coord)
		self.printintermediate(allreachable, "_")

		# Get the reachable target positions
		reachabletargets = [_ for _ in targetpositions if _ in allreachable]
		self.printintermediate(reachabletargets, "@")

		# Create a grid of all distances we can go to
		distances = self.floodfill(self.coord, allreachable)

		# Get the distances to the targets
		targetdistances = dict()
		for r in reachabletargets:
			targetdistances[r] = distances[r]

		if len(targetdistances) == 0:
			return

		# Get the minimum distance
		mindist = min(targetdistances.values())
		# Get the list of targets that are on min distance
		closesttargets = []
		for r in targetdistances.keys():
			if targetdistances[r] == mindist:
				closesttargets.append(r)
		# Sort them and get the first one.
		closesttarget = sorted(closesttargets)[0]
		#print("{0} will aim for {1} dist {2}".format(self, closesttarget, targetdistances[closesttarget]))

		# Now, get the distance map from the target to all nodes. 
		distances = self.floodfill(closesttarget, self.getreachable(closesttarget))

		if len(distances) == 0:
			print("reverse floodfill failed to yield")
			distances = {closesttarget: 0}
		#get the distances to the targets
		targetdistances = dict()
		for r in [_ for _ in self.adjacentcells() if _ in distances.keys()]: # No need to filter out occupied cells, as that will have been handled above
			targetdistances[r] = distances[r]
		#for r in targetdistances:
		#	print("{0}:{1}".format(r, targetdistances[r]))
		# Get the minimum distance
		mindist = min(targetdistances.values())
		closesttargets = []
		for r in targetdistances.keys():
			if targetdistances[r] == mindist:
				closesttargets.append(r)
		# Sort them and get the first one.
		firstmove = sorted(closesttargets)[0]

		self.coord = firstmove
		return

	def attack(self):
		# Get list of alive enemies
		enemies = self.getenemies()

		attackable = sorted([_ for _ in enemies if self.isadjacent(_)], key=lambda x:x.health)

		if len(attackable) > 0:
#			print("{0} attacks {1}".format(self, attackable[0]))
			attackable[0].injuredby(self)

	def injuredby(self, attacker):
		self.health -= attacker.attackpower
#		if not self.alive():
#			print("{0} died from attack by {1}".format(self, attacker))


	def tick(self):
		if not self.alive():
			return
		self.move()
		self.attack()


class Map:
	def __init__(self, mapname, elfpower):
		self.creatures = []
		self.grid = defaultdict(list)
		self.readgrid(mapname, elfpower)

	def readgrid(self, filename, elfpower):
		all=[_.strip() for _ in open(filename,'r').readlines()]
		power = {'E': elfpower, 'G': 3}
		for y in range(len(all)):
			for x in range(len(all[y])):
				c = all[y][x]
				if c in "EG":
					self.creatures.append(Creature(x, y, self, c, power[c])) 
					c = "."
				self.grid[y].append(c)

	def getcreature(self, coord):
		for c in self.livingcreatures():
			if c.onpos(coord):
				return c
		return None

	def isfloor(self, coord):
		#print(coord, len(self.grid[coord[1]]), self.grid[coord[1]])
		return self.grid[coord.y][coord.x] == "." 

	def isoccupied(self, coord):
		for c in self.livingcreatures():
			if c.onpos(coord):
				return True
		return False

	def getchar(self, coord):
		c = self.getcreature(coord)
		if c != None:
			return c.ctype
		return self.grid[coord.y][coord.x]

	def getprintablegrid(self):
		res = []
		for y in self.grid:
			r = []#["{0:2} ".format(y)]
			for x in range(len(self.grid[y])):
				r += self.getchar(Coordinate(x, y))
			res.append(r)
		return res

	def printgrid(self, grid=None):
		if grid == None:
			grid = self.getprintablegrid()
		for y in range(len(grid)):
			r = ""
			for x in grid[y]:
				r += x
			for c in sorted([_ for _ in self.livingcreatures() if _.coord.y == y]):
				r += " {0}({1}) ".format(c.ctype, c.health)
			print(r)
		print("---")

	def livingcreatures(self):
		return [_ for _ in self.creatures if _.alive()]

	def elvesdied(self):
		return len([_ for _ in self.creatures if _.ctype == "E" and not _.alive()]) > 0

	def creaturesoftype(self, ctype):
		return sorted([_ for _ in self.livingcreatures() if _.ctype == ctype])

	def elves(self):
		return self.creaturesoftype("E")
	def goblins(self):
		return self.creaturesoftype("G")

	def tick(self, round):
		res = True
		for c in sorted(self.livingcreatures()):
			c.tick()
			if len(self.elves()) == 0 or len(self.goblins()) == 0:
				res = False
#		print("Round", round)
#		self.printgrid()
		return res


def battle(m, elfpower):
#	m.printgrid()
	i = 0
	fullround = True
	while len(m.elves()) > 0 and len(m.goblins()) > 0:
		i += 1
		fullround = m.tick(i)
		if m.elvesdied():
			print("Elves lost one on", elfpower)
			return False
		#if i % 100 == 0:
#		print(i)

		#if i == 2: exit()

	if not fullround:
		i -= 1

#	m.printgrid()

	c = []
	if len(m.elves()) > 0:
		c = m.elves()
		print("Elves win!")
	else:
		c = m.goblins()
		print("Goblins win!")

	hp = [_.health for _ in c]
	score = sum(hp) * i
	print("hp:", hp, sum(hp))
	print("Total rounds", i)
	print("Score: {0} ({1})".format(score, sum(hp)*(i+1)))
	return True


filename = "15"
#filename = "15_1"
#filename = "15_2"
#filename = "15_3"
#filename = "15_3_23"
#filename = "15_8"
elfpower = 3
elveswon = False
while not elveswon:
	elfpower += 1
	m = Map(filename, elfpower)
	elveswon = battle(m, elfpower)
#m.printgrid()
print("Minimum elf power required:", elfpower)
