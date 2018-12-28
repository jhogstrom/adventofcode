from collections import defaultdict

class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.hash = hash(str(self))
	def __lt__(self, other):
		if self.y == other.y:
			return self.x < other.x
		return self.y < other.y

	def __eq__(self, other):
		if other == None: return False
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash(str(self))

	def __str__(self):
		return "({0},{1})".format(self.x, self.y)

	def new(self, dx, dy):
		return Coordinate(self.x + dx, self.y + dy)

	def adjacentcells(self):
		return [self.new(1, 0), self.new(-1, 0), self.new(0, 1), self.new(0, -1)]

class LineInfo:
	def __init__(self, line):
		#print(line)
		self.coords = dict()
		parts = [_.strip() for _ in line.split(",")]
		for p in parts:
			d = p.split("=")
			axis = d[0]
			isrange = False
			if ".." in d[1]:
				axisvalue = [_ for _ in range(int(d[1].split("..")[0]), int(d[1].split("..")[1])+1)]
			else:
				axisvalue = [_ for _ in range(int(d[1]), int(d[1])+1)]
			self.coords[axis] = axisvalue

	def __str__(self):
		s = ""
		for a in self.coords:
			s += a + ": " + str(self.coords[a]) + " "
		return s

	def fillgrid(self, grid, map):
		for y in self.coords['y']:
			map.ymin = min(map.ymin, y)
			map.ymax = max(map.ymax, y)
			for x in self.coords['x']:
				map.xmin = min(map.xmin, x)
				map.xmax = max(map.xmax, x)
				grid[y][x] = "#"


class Map:
	def __init__(self):
		self.ymin = 10000
		self.ymax = -10000
		self.xmin = 10000
		self.xmax = -10000
		row = lambda : defaultdict(lambda: ".")
		self.grid = defaultdict(row)
		self.grid[0][500] = "X"

		self.sources = [Coordinate(500, 0)]

	def readfile(self, filename):
		all=[_.strip() for _ in open(filename,'r').readlines()]
		for line in all:
			lInfo = LineInfo(line)
			lInfo.fillgrid(self.grid, self)

	def print(self, showsources=False):
		ystart = self.ymin - 1
		ystop = self.ymax + 2
		xstart = self.xmin - 1
		xstop = self.xmax + 2
		yminsource = ymaxsource = 0
		WIDTH = 10

		if showsources:
			allx = [_.x for _ in self.sources]
			if len(allx) > 0:
				xstart = max(xstart, min(allx) - WIDTH)
				xstop = min(xstop, max(allx) + WIDTH)
			ally = [_.y for _ in self.sources]
			if len(ally) > 0:
				yminsource = min(ally)
				ymaxsource = max(ally)
				ystop = ymaxsource + WIDTH


		for y in range(ystart, ystop):
			r = "{0:4} ".format(y)
			for x in range(xstart, xstop):
				if showsources and y >= yminsource and y <= ymaxsource and x >= xstart + WIDTH and x <= xstop - WIDTH and Coordinate(x, y) in self.sources:
					r += "V"
				else:
					r += self.grid[y][x]
			print(r)

	def atpos(self, pos):
		return self.grid[pos.y][pos.x]

	def setatpos(self, pos, c):
		self.grid[pos.y][pos.x] = c

	def hasbounds(self, src):
		#print("Checking", src, self.xmax)
		p = src.new(0, 0)
		res = True

		while p.x >= self.xmin - 1:
			#print("Left/Below", p, self.atpos(p.new(0, 1)))
			if self.atpos(p) == "#": break
			if self.atpos(p.new(0, 1)) == ".": return False
			p.x -= 1
		#print(p, src)
		p.x = src.x
		while p.x <= self.xmax+1:
			#print("Right/Below", p, self.atpos(p.new(0, 1)))
			if self.atpos(p) == "#": break
			if self.atpos(p.new(0, 1)) == ".": return False
			p.x += 1
		return res

	def followsource(self, src):
		def movehoriz(pos, dir, cond):
			#print("move left", s)
			while not self.atpos(pos) in "#" and cond(s.x):
				self.setatpos(s, "~")
				s.x += dir
				#print("left", s)

		# Move down while we move through sand
		while self.atpos(src) in ".X":
			self.setatpos(src, "|")
			src.y += 1
			if src.y > self.ymax: return [None]
			#print("down", src)
		src.y -= 1

		# If we dropped into a filled bucket, then someone else has already done our job
		if self.atpos(src) == '~':
			return [None]
		# Fill bucket (as indicated by hasbounds!) until we can overflow in some direction
		s = src.new(0, 0)
		while self.hasbounds(s.new(0, 0)):
			# go left
			#print("move left", s)
			movehoriz(s, -1, lambda _:_ >= self.xmin-1)
			s.x = src.x
			# go right
			movehoriz(s, 1, lambda _:_ <= self.xmax+1)
			s.x = src.x
			s.y -= 1
		src.y = s.y

		# Fill surface until we hit wall or free fall.
		#print("Overflowing from", s)
		res = []

		# go left
		#print("move left", s)
		while not self.atpos(s) in "#" and not self.atpos(s.new(0, 1)) in '.|' and s.x >= self.xmin-1:
			self.setatpos(s, "|")
			s.x -= 1
			#print("left", s)
		if not self.atpos(s) in "#|" and s.x >= self.xmin-1:
			res.append(s.new(0, 0))
		s.x = src.x
		# go right
		#print("move right", s)
		while not self.atpos(s) in "#" and not self.atpos(s.new(0, 1)) in '.|' and s.x <= self.xmax + 1:
			self.setatpos(s, "|")
			s.x += 1
			#print("right", s)
		if not self.atpos(s) in "#|" and s.x < self.xmax:
			res.append(s.new(0, 0))

		return res

	def debugprintround(self, c):
#		for _ in self.sources:
#			print(_)
		print("vvvvv", c)
#		self.print(showsources=True)
		if len(self.sources) > 0:
			my = max([_.y for _ in self.sources])
			mxx = max([_.x for _ in self.sources])
			mix = min([_.x for _ in self.sources])
			print("=== {0} - {1} (sources: {2} y:{3}/{4} x:{5}-{6}/{7}-{8})".\
				format(c, self.countwater(), len(self.sources), my, self.ymax,\
					mix, mxx, self.xmin, self.xmax))


	def followsources(self):
		c = 0
		seen = []
		while len(self.sources) > 0:
			c += 1
			newsources = []
			for s in self.sources:
				ns = self.followsource(s)
				newsources += [_ for _ in ns if _ != None and _.y <= self.ymax]

			self.sources = [src for src in set(newsources) if not src in seen]
			seen += self.sources

			self.debugprintround(c)

			if c == 200: 
				print("Count stop")
				return

	def countchars(self, chars):
		res = 0
		for y in range(self.ymin, self.ymax+1):
			for x in range(self.xmin-2, self.xmax+2):
				if self.grid[y][x] in chars:
					res += 1
		return res

	def countwater(self):
		return self.countchars("~|")

	def countremainingwater(self):
		return self.countchars("~")
			
filename = "17"

m = Map()
m.readfile(filename)
#m.print()
m.followsources()


print("Water:", m.countwater())
print("Remaining Water:", m.countremainingwater())


#Water: 57
#Remaining Water: 29

#Water: 40879
#Remaining Water: 34693