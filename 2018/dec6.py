from collections import defaultdict
import math 
all=[ s.strip() for s in open('6','r').readlines()]

testdata = [
"1, 1",
"1, 6",
"8, 3",
"3, 4",
"5, 5",
"8, 9"]

all = testdata

row = tree = lambda: defaultdict(list)
grid = defaultdict(row)
miny=minx=10000
maxy=maxx=0
coords = []

def readcoords():
	print("reading")
	global minx, miny, maxx, maxy
	c = 0
	for s in all:
		x, y = [int(_.strip()) for _ in s.split(",")]
		grid[y][x] = [c, defaultdict(int)]
		miny = min(miny, y)
		minx = min(minx, x)
		maxx = max(maxx, x)
		maxy = max(maxy, y)
		c += 1
		coords.append([x, y])
#		print(x, y, minx, maxx, miny, maxy)

def fillgrid():
	print("filling")
	for y in range(miny-1, maxy+2):
		for x in range(minx-1, maxx+2):
			if len(grid[y][x]) == 0:
				grid[y][x] = [-1, defaultdict(int)]

def printgrid():
	for y in range(miny-1, maxy+2):
		r = ""
		for x in range(minx-1, maxx+2):
			if grid[y][x][0] == -1:
				r += "."
			else:
				r += "X"
		print(r)
	print()

def manhattandist(x, y, coord):
	return abs(x - coord[0]) + abs(y - coord[1])

def allmanhattandist():
	print("allmanhattandist")
	for y in range(miny-1, maxy+2):
		for x in range(minx-1, maxx+2):
			i = 0
			while i < len(coords):
				grid[y][x][1][i] = manhattandist(x, y, coords[i])
				i += 1

distgrid = defaultdict(list)
def calcgrid():
	print("calcgrid")
	for y in range(miny-1, maxy+1):
		r = ""
		for x in range(minx-1, maxx+2):
			eq = False
			mindist = 1000
			closest = ""
			for c in grid[y][x][1]:
				#print(x, y, c)
				if mindist == grid[y][x][1][c]:
					eq = True
				if grid[y][x][1][c] < mindist:
					closest = c
					mindist = grid[y][x][1][c]
					eq = False
			if eq:
				r += " .. "
				distgrid[y].append(-1)
			else:
				r += " " + str(closest).zfill(2) + " "
				distgrid[y].append(closest)
		print(r)

	print("get frequency")
	print(miny, maxy)
	print(minx, maxx)
	freq = defaultdict(int)
	for y in range(miny-1, maxy+1-miny):
		for x in range(minx-1, maxx+2-minx):
			#print(x, y)
			#print(distgrid[y][x])
			#print("=>", freq[distgrid[y][x]])
			freq[distgrid[y][x]] += 1

	print("reset infinite")

#	for y in distgrid:
#		print(distgrid[y])
#	print(sum(freq.values()))
#
#	print(freq)

	for r in distgrid:
		print("{0:3}/{2} => {1}".format(r, distgrid[r][:10], len(distgrid[r])))
	print(max(freq.values()))
	print(freq)
	for x in range(minx-1, maxx + 2 - minx):
		freq[distgrid[miny][x]] = 0
		freq[distgrid[maxy][x]] = 0 #len(distgrid)-1
	for y in distgrid:
		#print(y)
		freq[distgrid[y][minx]] = 0
		freq[distgrid[y][maxx-1-miny]] = 0 #len(distgrid)-1
	print(freq)
	print(max(freq.values()))			

def calctotaldist():
	minbucket = defaultdict(int)
	MAXSIZE = 32
	for y in grid:
		for x in grid[y]:
			totaldist = sum(grid[y][x][1].values())
			#if totaldist < MAXSIZE:
			minbucket[totaldist] += 1
			print("{0}:{1}: {2}".format(x, y, totaldist))
	largestarea = 0

	for b in minbucket:
		print("min[{0}] => {1}".format(b, minbucket[b]))
	print("Sum(buckets)", sum(minbucket.values()))
	for i in minbucket:
		if minbucket[i] > largestarea:
			largestarea = minbucket[i]

	print("Largest area: ", largestarea)

readcoords()
fillgrid()
printgrid()
#printgrid()
allmanhattandist()
calcgrid()
#calctotaldist()
