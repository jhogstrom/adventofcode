from collections import defaultdict
all=[ s.strip() for s in open('3','r').readlines()]
row = tree = lambda: defaultdict(list)
cloth = defaultdict(row)
doub = 0

testdata = [
"#123 @ 1,3: 4x4",
"#2 @ 3,1: 4x4",
"#3 @ 5,5: 2x2"
]

ids = defaultdict(bool)
#all = testdata
for s in all:
	id,_,coord,grid = s.split()
	id = id[1:]
	x,y = [int(_) for _ in coord[:len(coord)-1].split(",")]
	sx,sy = [int(_) for _ in grid.split("x")]

	ids[id] = True
	for i in range(x, x+sx):
		for j in range(y, y+sy):
			cloth[j][i].append(id)

for y in range(len(cloth)):
	for x in range(len(cloth)):
		l = len(cloth[y][x])
		if l > 1:
			doub += 1
			for i in cloth[y][x]:
				ids[i] = False

print("doubles:", doub)

for i in ids:
	if ids[i]:
		print("Remains: ", i)


	