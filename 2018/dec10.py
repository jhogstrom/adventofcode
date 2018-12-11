from collections import defaultdict
filename,ITER="10ex", 10
filename, ITER="10", 10420
all=[ s.strip() for s in open(filename,'r').readlines()]

class Cell(object):
	def __init__(self, p, v):
		self.pos = p
		self.vel = v

	def move(self):
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]

	def matches(self, x, y):
		return self.pos[1] == x and self.pos[0] == y

def matchchar(cells, x, y):
	for _ in cells:
		if _.matches(x, y):
			return "#"
	return " "

def movecells(cells):
	for _ in cells:
		_.move()

def printstars(cells):
	xrnge = [min([_.pos[0] for _ in cells]), max([_.pos[0] for _ in cells])]
	yrnge = [min([_.pos[1] for _ in cells]), max([_.pos[1] for _ in cells])]
	xlen = abs(xrnge[0]) + abs(xrnge[1])
	ylen = abs(yrnge[0]) + abs(yrnge[1])
	print(xrnge, yrnge, xlen, ylen)
	#exit()

	for i in range(ITER):
		movecells(cells)
		if ITER > 10000:
			if i % 500 == 0:
				print(i)
			if i < 10410:
				continue
			if i % 10 == 0:
				print(i)
		res = []
		cxmin = min([_.pos[0] for _ in cells])
		cxmax = max([_.pos[0] for _ in cells])
		cymin = min([_.pos[1] for _ in cells])
		cymax = max([_.pos[1] for _ in cells])

		for y in range(cymin, cymax + 1):
			g = list(" " * (1 + abs(cxmin) + abs(cxmax)))
			hasstar = False
			for c in cells:
				if c.pos[1] == y:
					#print(x, c.pos[1] + cymin, len(g))
					g[c.pos[0] + abs(cxmin)] = "#"
					hasstar = True
			if hasstar:
				r = "".join(g)
				if r.rstrip() != "":
					res.append(r)

		doprint = False
		for r in res:
			if "#####" in r:
				doprint = True
				break
		if doprint:
			for r in res:
				print(r)
			print(i, "---")


stars = []
		
for s in all:
	s = s.split("> ")
	p = [int(_) for _ in s[0][10:].split(",")]
	v = [int(_) for _ in s[1][10:-1].split(",")]
	#print(p, v)
	stars.append(Cell(p, v))

printstars(stars)
