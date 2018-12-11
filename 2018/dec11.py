from collections import defaultdict
serial = 3031
#serial = 42
#serial = 18

SIZE=300
SEARCHAREA=50

def powerlevel(x, y, s):
	v = x
	v = x + 10
	v *= y
	v += s
	v *= (x+10)
	return int(str(v).zfill(3)[-3:-2]) - 5

#print(powerlevel(3, 5, 8))

#print(powerlevel(122, 79, 57))
#print(powerlevel(217, 196, 39))
#print(powerlevel(101, 153, 71))
#exit()


def creategrid():
	grid = defaultdict(list)
	for y in range(SIZE):
		for x in range(SIZE):
			grid[y].append(powerlevel(x+1, y+1, serial))
	return grid

def addgridsums(grid):
	row = tree = lambda: defaultdict(list)
	gridsum = defaultdict(row)
	for y in range(SIZE):
		for x in range(SIZE):
			gridsum[y][x] = []
#			print(grid[y][x:10])
			for i in range(x+1, x+1+SEARCHAREA):
#				if i < 10:
#					print(x, i, sum(grid[y][x:i]), grid[y][x:i])
				gridsum[y][x].append(sum(grid[y][x:i]))
#			gridsum[y].append(sum(grid[y][x:x+3]))
		if y % 50 == 0:
				print("added", y)
	return gridsum

def getareavalue(gridsum, x, y, size):
	if x + size >= SIZE:
		return 0
	s = 0
	for dy in range(y, min(SIZE, y+size)):
		#print(dy, x)
		s += gridsum[dy][x][size-1]
	#s = gridsum[y][x][size-1] + gridsum[y+1][x][size-1] + gridsum[y+2][x][size-1]
	return s

def findmax(grid, gridsum):
	maxval = 0
	savex, savey, maxsize = 0, 0, 0
	for y in range(SIZE):
		if y % 50 == 0:
			print("scanned", y)
		for x in range(SIZE):
			for i in range(1, SEARCHAREA):
				s = getareavalue(gridsum, x, y, i)
				if s > maxval:
					maxval = s
					savex = x
					savey = y
					maxsize = i
	return [savex+1, savey+1, maxval, maxsize]

def printsector(grid, coord, size):
	for y in range(coord[1]-1, coord[1]+size+1):
		r = ""
		for x in range(coord[0]-1, coord[0]+size+1):
			fstr = " {0:2} "
			if x in range(coord[0], coord[0]+size) and y in range(coord[1], coord[1]+size):
				fstr = "[{0:2}]"

			r += fstr.format(grid[y-1][x-1])
		print(r)

grid = creategrid()
gridsum = addgridsums(grid)
res = findmax(grid, gridsum)
printsector(grid, res, res[-1])

print("Result:", res)

print("{0},{1},{2}".format(res[0], res[1], res[3]))