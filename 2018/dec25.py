from collections import defaultdict

filename = "25"
all=[_.strip() for _ in open(filename,'r').readlines()]

class Coordinate:
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.t = t

	def mhdist(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.t - other.t)

coords = []
for l in all:
	c = [int(_) for _ in l.split(",")]
	coords.append(Coordinate(c[0], c[1], c[2], c[3]))

def fitingroup(coord, groups):
	res = []
	for g in groups:
		for c in groups[g]:
			if coord.mhdist(c) <= 3:
				res.append(g)
				break
	return res

groups = defaultdict(list)

for c in coords:
	g = fitingroup(c, groups)
	if len(g) == 0:
		groups[len(groups)].append(c)
	elif len(g) == 1:
		groups[g[0]].append(c)
	else:
		for i in g[1:]:
			groups[g[0]] += groups[i]
			groups[i] = []
		groups[g[0]].append(c)

#for g in groups:
#	print("{0} - {1}".format(g, [str(_) for _ in groups[g]]))

res = len([_ for _ in groups if len(groups[_]) > 0])
ccount = sum([len(groups[_]) for _ in groups])

print("Groups: {0} ({1})".format(res, ccount))