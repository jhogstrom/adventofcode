from collections import defaultdict
serial = 3031
grid = defaultdict(list)
gridsum = defaultdict(list)

def powerlevel(x, y, s):
	v = x
	v = x + 10
	v *= y
	v += s
	v *= (x+10)
	return int(str(v).zfill(5)[-3:-2]) - 5

#print(powerlevel(3, 5, 8))

#print(powerlevel(122, 79, 57))
#print(powerlevel(217, 196, 39))
#print(powerlevel(101, 153, 71))
#exit()


for y in range(300):
	for x in range(300):
#		v = x+1
#		v = x + 10
#		v *= (y+1)
#		v += serial
#		v *= (x+10)
#		v = str(v).zfill(5)[-3:-2]
		#v = int(str((((x+10)*y)+serial)*(x+10)).zfill(5)[-3:-2])
		grid[y].append(powerlevel(x+1, y+1, serial))


maxval = 0
savex, savey = 0, 0
for y in range(300):
	for x in range(300-3):
		gridsum[y].append(sum(grid[y][x:x+3]))

#print(len(gridsum[1]))
#print(gridsum[1])
#exit()
for y in range(300-3):
	if y % 50 == 0:
		print(y)
	for x in range(300-3):
#		print(x, y, len(gridsum[y]))
		s = gridsum[y][x] + gridsum[y+1][x] + gridsum[y+2][x]
		if s > maxval:
			maxval = s
			savex = x
			savey = y


print("{0},{1}".format(savex+1, savey+1))

for y in range(savey - 3, savey + 6):
	r = ""
	for x in range(savex - 3, savex + 6):
		r += " {0:3} ".format(grid[y][x])
	print(r)
