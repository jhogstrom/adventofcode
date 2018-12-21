from collections import defaultdict
import sys

directions = {
	'E': [ 1,  0, '|'], 
	'W': [-1,  0, '|'], 
	'N': [ 0, -1, '-'], 
	'S': [ 0,  1, '-']}
class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.hash = hash(str(self))
	def __lt__(self, other):
		if self.y == other.y:
			return self.x < other.x
		return self.y < other.y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return self.hash#hash(str(self))

	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def new(self, dx, dy):
		return Coord(self.x + dx, self.y + dy)

	def adjacentcells(self, dist=1):
		return [self.new(dist, 0), self.new(-dist, 0), self.new(0, dist), self.new(0, -dist)]

class World:
	def __init__(self):
		defaultvalue = lambda: '#'
		row = lambda: defaultdict(defaultvalue)
		self.grid = defaultdict(row)
		self.pos = Coord(0, 0)
		self.makeroom(self.pos)

	def makewall(self, coord):
		self.grid[coord.y][coord.x] = "#"

	def makedoor(self, coord, door='?'):
		if self.grid[coord.y][coord.x] in '-|':
			return
		self.grid[coord.y][coord.x] = door

	def makeroom(self, coord):
		self.grid[coord.y][coord.x]="."
		self.makewall(coord.new(-1, -1))
		self.makedoor(coord.new(-1, 0))
		self.makewall(coord.new(-1, 1))

		self.makewall(coord.new(1, -1))
		self.makedoor(coord.new(1, 0))
		self.makewall(coord.new(1, 1))

		self.makedoor(coord.new(0, -1))
		self.makedoor(coord.new(0, 1))

	def printgrid(self, data=None, datafunc=None):
		def xforself(x, y, g, data):
			return g.pos == Coord(x, y)

		if datafunc==None:
			datafunc = xforself

		ymin = min(self.grid.keys())
		ymax = max(self.grid.keys())
		xmax = 0
		xmin = 10000
		for y in self.grid:
			xmin = min(xmin, min(self.grid[y]))
			xmax = max(xmax, max(self.grid[y]))

		for y in range(ymin, ymax+1):
			r = ">"
			for x in range(xmin, xmax + 1):
				if datafunc(x, y, self, data):
					r += 'X'
				else:
					r += self.grid[y][x]
			r += "<"
			print(r)
		print("===")

	def createwalk(self, dir):
		d = directions[dir]
		p = self.pos.new(d[0], d[1])
		self.makedoor(p, d[2])
		self.pos = p
		p = self.pos.new(d[0], d[1])
		self.makeroom(p)
		self.pos = p

	def walk(self, dir):
		d = directions[dir]
		self.pos = self.pos.new(d[0]*2, d[1]*2)
#		print("walked {0} => {1}".format(dir, self.pos))

	def canwalk(self, pos, dir):
		d = directions[dir]
		p = pos.new(d[0], d[1])
		return self.grid[p.y][p.x] != "#"

	def wallifydoors(self):
		for y in self.grid:
			for x in self.grid[y]:
				if self.grid[y][x] == '?':
					self.grid[y][x] = "#"

	def gridarea(self):
		return len(self.grid) * len(self.grid[0])

	def floodfill(self, startcoord):
		mapped = defaultdict()
		def fill(nodes, dist):
			edge = []
			for n in nodes:
				if (not n in mapped) or (mapped[n] > dist):
					mapped[n] = dist
					edge += [_ for _ in n.adjacentcells() if not self.grid[_.y][_.x] == "#"]
			return edge

		newnodes = [_ for _ in startcoord.adjacentcells() if not self.grid[_.y][_.x] == "#"]
		dist = 0
		while len(newnodes) > 0:
			#print(newnodes)
			dist += 1
			newnodes = fill(newnodes, dist)
		mapped[startcoord] = 0
		return mapped


stack = []
def walk(w, path):
	for c in path:
		if c in "^$":
			continue
		if c == "(":
			stack.append(w.pos)
		elif c == ")":
			stack.pop()
		elif c == "|":
			w.pos = stack[-1]
		else:
			w.createwalk(c)
	w.wallifydoors()
	w.pos = Coord(0, 0)


defaultint = lambda: False
row = lambda: defaultdict(defaultint)
doorgrid = defaultdict(row)

def isonpath(x, y, g, data):
	return data[y][x]

doormax = 0
# The recursive way worked, but not on big maps. Moved to floodfill
def traverse(w, pos, doors, path):
	global doormax
	doorgrid[pos.y][pos.x] = doors
	doormax = max(doormax, doors)
#	print("Setting {0} => {1}".format(pos, doors))
#	w.printgrid(doorgrid, isonpath)
	for dir in "NESW":
		d = directions[dir]
		c = pos.new(d[0]*2, d[1]*2)
		dc = doorgrid[c.y][c.x]
#		print(dc, doors, c)
		if (not c in path) and w.canwalk(pos, dir) and (not dc or dc > doors):
			traverse(w, c, doors + 1, path + [w.pos])


exp = "?"	
all, exp = "^WNE$", 3
#all, exp = "^ENWWW(NEEE|SSE(EE|N))$", 10
#all, exp = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18
#all, exp = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23
#all, exp = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31
all = open("20",'r').readline()

w = World()
walk(w, all)
#w.printgrid()
#traverse(w, w.pos, 0, [w.pos])
mapped = w.floodfill(w.pos)
#Problem with floodfill is that is counts all steps, including walls.
# That's gives us an answer that's too high. By two.
# To count how many rooms are a certain door-distance away, 
# first we remove all cells that aren't rooms.
# ALso divide their distance by two as we are indeed a factor two off.
newmapped = defaultdict(int)
for n in mapped:
	if w.grid[n.y][n.x] == ".":
		newmapped[n] = mapped[n] // 2

# Now the largest number of doors can be extracted
print("Got {0}, expected {1}".format(max(newmapped.values()), exp))

# As well as rooms that are at least 1000 doors away.
print("Rooms at least 1000 doors away: {0}".format(len([_ for _ in newmapped.values() if _ >= 1000])))
