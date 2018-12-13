from collections import defaultdict

NS = "|"
EW = "-"
LT = "\\"
RT = "/"
INTSCT = "+"

mapchar = dict()
mapchar[NS] = 0
mapchar["v"] = 0
mapchar["^"] = 0
mapchar[EW] = 1
mapchar["<"] = 1
mapchar[">"] = 1
mapchar[LT] = 2
mapchar[RT] = 3
mapchar[INTSCT] = 4
mapchar[" "] = 5
directions = "<^>v"
turns=[3, 0, 1]

class Car:
	def __init__(self, x, y, c, grid, cars):
		print("Creating car going {0} on {1}/{2}".format(c, x, y))
		self.x = x
		self.y = y
		self.direction = directions.index(c)
		self.lastturn = 2 # First turn is LEFT, and we'll increase before we turn.
		self.grid = grid
		self.cars = cars
		self.eliminated = False
	def maketurn(self):
		turn = (self.lastturn + 1) % 3
		self.direction += turns[turn]
		self.direction %= 4
		self.lastturn = turn
	def turnleft(self):
		self.direction += 3
		self.direction %= 4
	def turnright(self):
		self.direction += 1
		self.direction %= 4
	def move(self):
		if self.eliminated:
			return
		if self.direction == directions.index("<"): self.x -= 1
		elif self.direction == directions.index(">"): self.x += 1
		elif self.direction == directions.index("^"): self.y -= 1
		elif self.direction == directions.index("v"): self.y += 1
		else: raise

		if self.grid[self.y][self.x] == "/":
			if self.direction == directions.index(">"): 
				self.turnleft()
			elif self.direction == directions.index("<"): 
				self.turnleft()
			elif self.direction == directions.index("^"): 
				self.turnright()
			elif self.direction == directions.index("v"):
				self.turnright()
		elif self.grid[self.y][self.x] == "\\":
			if self.direction == directions.index(">"):
				self.turnright()
			elif self.direction == directions.index("<"): 
				self.turnright()
			elif self.direction == directions.index("^"): 
				self.turnleft()
			elif self.direction == directions.index("v"): 
				self.turnleft()
		elif self.grid[self.y][self.x] == "+":
			self.maketurn()

#		self.detectcollission()
		self.removecolliders()

	def detectcollission(self):
		for c in self.cars:
			if c != self and c.x == self.x and c.y == self.y:
				print("COLLIDE: {0},{1}".format(self.x, self.y))
				exit()	

	def removecolliders(self):
		for c in self.cars:
			if c.eliminated:
				continue
			if (c != self) and ((c.x == self.x) and (c.y == self.y)):
#				print("Colliding {0},{1} ({2}) <-> {3},{4} ({5})"
#					.format(self.x, self.y, directions[self.direction], c.x, c.y, directions[c.direction]))
				c.eliminated = True
				self.eliminated = True

	def __lt__(self, other):
		if self.y == other.y:
			return self.x < other.x
		return self.y < other.y

	def atpos(self, x, y):
		return self.x == x and self.y == y


def readdata(filename):
	grid = defaultdict(list)
	cars = []
	all=[s for s in open(filename,'r').readlines()]
	for r in range(len(all)):
		for c in all[r]:
			if c in "<>^v":
				cars.append(Car(len(grid[r]), len(grid)-1, c, grid, cars))
			if c in "<>": c = "-"
			if c in "v^": c = "|"
			if c in "\\/-|+ ":
				grid[r].append(c)
	return grid, sorted(cars)

def printcars(cars):
	print([[_.x, _.y, directions[_.direction]] for _ in cars])	

def printgrid(grid, cars):
	for y in range(len(grid)):
		r = ""
		for x in range(len(grid[y])):
			hascar = False
			curcar = []
			for c in cars:
				if c.atpos(x, y):
					hascar = True
					curcar.append(c)
					
			if curcar == []:
				r += grid[y][x]
			elif len(curcar) == 1:
				r += directions[curcar[0].direction]
			else:
				r += "X"
		print(r[:80])
	print("---")

def tick():
	for c in sorted(cars):
		if not c.eliminated:
			c.move()
		remains = []
		for k in cars:
			if not k.eliminated:
				remains.append(k)

		if len(remains) == 1:
			k = remains[0]
			k.move() # At this point we don't know if the remainding car has moved or not.
			print("Lastman standing: ", k.x, k.y, directions[k.direction])
			exit()


filename="13"
#filename="13ex"
#filename="13ex2"
grid, cars = readdata(filename)

for i in range(20000):
	tick()