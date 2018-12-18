from collections import defaultdict

def readarea():
	all = [_.strip() for _ in open("18",'r').readlines()]
	area = defaultdict(list)
	for y in range(len(all)):
		for x in range(len(all[y])):
			area[y].append(all[y][x])
	return area

def areavalue(area):
	tree, lumber = 0, 0
	for y in area:
		for x in area[y]:
			if x == "|": tree += 1
			if x == "#": lumber += 1
	return tree, lumber, tree * lumber

def printarea(area, minutes):
	if minutes % 1000 == 0:
		print("After {0} minutes".format(minutes))
		for y in area:
			r = ""
			for x in area[y]:
				r += x
			print(r)
		print("===")
		print(areavalue(area))

def ischar(x, y, area, c):
	if y < 0: return 0
	if y >= len(area): return 0
	if x < 0: return 0
	if x >= len(area[y]): return 0
	if area[y][x] == c:
		return 1
	return 0

def neighbours(x, y, area, c):
	count = 0
	count += ischar(x-1, y-1, area, c)
	count += ischar(x-1, y, area, c)
	count += ischar(x-1, y+1, area, c)

	count += ischar(x+1, y-1, area, c)
	count += ischar(x+1, y, area, c)
	count += ischar(x+1, y+1, area, c)
	
	count += ischar(x, y-1, area, c)
	count += ischar(x, y+1, area, c)
	return count


def oneminute(org):
	area = defaultdict(list)
	for y in range(len(org)):
		for x in range(len(org[y])):
			c = org[y][x]
			if c == "." and neighbours(x, y, org, "|") >= 3:
				c = "|"
			elif c == "|" and neighbours(x, y, org, "#") >= 3:
				c = "#"
			elif c == "#":
				if (neighbours(x, y, org, "#") >= 1 and neighbours(x, y, org, "|")) >= 1:
					c = "#"
				else:
					c = "."
			area[y].append(c)
	return area

area = readarea()
areas = []

last = diff = 0

for i in range(1000):
	area = oneminute(area)
	# if we've seen the area before, 
	# get the diff from current to first instance of the area
	# remember when we saw the first repetition
	if area in areas:
		diff = i - areas.index(area)
		print(i, diff)
		last = i
		break
	else:
		areas.append(area)

# Now loop MAX-last mod diff to get the area value of MAX
for i in range(((1000000000-last)%diff)-1):
	area = oneminute(area)

printarea(area, i)
print(areavalue(area))