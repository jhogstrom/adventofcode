from collections import defaultdict
all=open('5','r').readline().strip()

testdata = "dabAcCaCBAcCcaDA"
testdata = "abbadabAcCaCBAcCcaDAabbaad"

#all = testdata
#all = "aabAAB"
#all = "dabAcCaCBAcCcaDA"
print(len(all))


def polymerize(all):
	i = 0
	while i < len(all)-1:
		c1, c2 = all[i], all[i+1]
		if (c1 == c2.upper() or c1.upper() == c2) and c1 != c2:
	#		print("removed {0} at {1}".format(c1 + c2, i))
			all = all[:i] + all[i+2:]
	#		print("=> {0}".format(all))
			i = max(0, i-1)
		else:
			i += 1
	return len(all)

def removeunit(c, s):
	r, i, c = "", 0, c.upper()
	while i < len(s):
		if c != s[i].upper():
#			print("removing {0} at {1}".format(s[i], i))
			r += s[i]
		i += 1
	return r

cmin, rmin = "", rmin

for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
	r = polymerize(removeunit(c, all))
	print(c, r)
	if r < rmin:
		rmin, cmin = r, c

print("=> {0} - {1}".format(cmin, rmin))
#print(polymerize(all))
#print(all)
#print(removeunit('a', all))

