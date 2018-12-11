from collections import defaultdict
import math 
all=[ s.strip() for s in open('6','r').readlines()]
MAXSIZE = 10000

testdata = [
"1, 1",
"1, 6",
"8, 3",
"3, 4",
"5, 5",
"8, 9"]

#all, MAXSIZE = testdata, 32

row = tree = lambda: defaultdict(list)
grid = defaultdict(row)
miny=minx=10000
maxy=maxx=0
coords = []

class Cell:
	def __init__(self, isCoord, coord):
		self.isCoord = isCoord
		self.coord = coord
		self.manhattandists = []
		self.mindist = 1000
		self.closest = -1
		self._totalmhdist = -1
	def asChar(self):
		if not self.isCoord:
			return "."
		return "X"
	def asDist(self):
		if self.mindist == -1:
			return " .. "
		return " {0:2} ".format(self.closest)

	def calcmindist(self):
		d = [_[1] for _ in self.manhattandists]

		self.mindist = min(d)

		if d.count(self.mindist) != 1:
			self.mindist = -1
		else:
			self.closest = d.index(m)

	def totalmhdist(self):
		if self._totalmhdist == -1:
			self._totalmhdist = sum([_[1] for _ in self.manhattandists])
		return self._totalmhdist


def readcoords():
	print("reading")
	global minx, miny, maxx, maxy
	for s in all:
		coords.append([int(_.strip()) for _ in s.split(",")])
	x = [_[0] for _ in coords]
	y = [_[1] for _ in coords]
	maxx, minx = max(x)+2, min(x)-1
	maxy, miny = max(y)+1, min(y)-1

def fillgrid():
	print("filling")
	for y in range(miny, maxy-miny):
		for x in range(minx, maxx):
			if [x, y] in coords:
				c = coords.index([x, y])
			else:
				c = -1
			grid[y][x] = Cell([x, y] in coords, c)

def printgrid():
	for y in grid:
		r = ""
		for x in grid[y]:
			r += grid[y][x].asChar()
		print(r)
	print()

def printdistfield():
	for y in grid:
		r = ""
		for x in grid[y]:
			r += "{0:3} ".format(grid[y][x][2])
		print(r)
	print()

def manhattandist(x, y, coord):
	return abs(x - coord[0]) + abs(y - coord[1])

def allmanhattandist():
	print("allmanhattandist")
	for y in grid:
		for x in grid[y]:
			for c in coords:
				grid[y][x].manhattandists.append([coords.index(c), manhattandist(x, y, c)])


def printdistances():
	print("vvv Distances")
	for y in grid:
		r = ""
		for x in grid[y]:
			r += grid[y][x].asDist()
		print(r)
	print("^^^ Distances")

def calcgrid():
	print("calcgrid")
	for y in grid:
		for x in grid[y]:
			grid[y][x].calcmindist()

#	printdistances()
	print("get frequency")
	freq = defaultdict(int)
	for y in grid:
		for x in grid[y]:
			if grid[y][x].mindist != -1:
				freq[grid[y][x].closest] += 1
			#print(grid[y][x].closest)

	print("reset infinite")

	ymi = min(grid.keys())
	yma = max(grid.keys())
	xmi = min(grid[ymi].keys())
	xma = max(grid[ymi].keys())
	for x in range(minx, maxx - minx):
		freq[grid[ymi][x].closest] = 0
		freq[grid[yma][x].closest] = 0 
#		print("Resetting {0}:{1} ({4})|| {2}:{3} ({5})"
#			.format(x, ymi, x, yma, grid[ymi][x].closest, grid[yma][x].closest))
	for y in grid:
		freq[grid[y][xmi].closest] = 0
		freq[grid[y][xma].closest] = 0
#		print("Resetting {0}:{1} ({4})|| {2}:{3} ({5})"
#			.format(xmi, y, xma, y, grid[y][xmi].closest, grid[y][xma].closest))
	print("Largest area with smallest distance: ", max(freq.values()))
	for f in freq:
		if freq[f] != 0:
			print(f, freq[f])

def calctotaldist():
	minbucket = defaultdict(int)
	area = 0
	for y in grid:
		for x in grid[y]:
			if grid[y][x].totalmhdist() < MAXSIZE:
				#print(x, y, )
				area += 1
				minbucket[grid[y][x].totalmhdist()] += 1
	print("Largest area under {0} is {1}".format(MAXSIZE, area))				
	

	for b in minbucket:
		print("min[{0}] => {1}".format(b, minbucket[b]))
	print("Sum(buckets)", sum(minbucket.values()))
	largestarea = max(minbucket)

	print("Largest area: ", largestarea)
	print("Largest area in total: ", area)
	print("Should be larger than 41542")

readcoords()
fillgrid()
#printgrid()
allmanhattandist()
#calcgrid()
calctotaldist()
#printdistfield()