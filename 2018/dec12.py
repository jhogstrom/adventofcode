from collections import defaultdict


inp="##..#..##.#....##.#..#.#.##.#.#.######..##.#.#.####.#..#...##...#....#....#.##.###..#..###...#...#.."

all=[s.strip() for s in open('12','r').readlines()]
rules = dict()
for s in all:
	_=s.split(" => ")
	rules[_[0]] = _[1]

#for r in rules:
#	print(r, rules[r])

leftmost = 0

#print(inp)
def addempty(s):
	global leftmost
	while s[:3] != "...":
		s = "." + s
		leftmost += 1
	while s[-3:] != "...":
		s += "."
	i = 0
	while s[i:i+7] == ".......":
		i += 1
		leftmost -=1
	return s[i:]

def generate(inp):
	inp = addempty(inp)
	r = ".."
	for i in range(2, len(inp)-2):
		c = inp[i-2:i+3]
		#print(i-2, i+3, c, len(r)) 
		if c in rules:
			r += rules[c]
	#		print("Rulematch:", c, "=>", rules[c], r)
		else:
			r += inp[i]

	return addempty(r)

def countpots(s):
	res = 0
	for c in s:
		if c == "#":
			res += 1
	return res

def calcsumpots(s, leftmost):
	res = 0
	for i in range(len(s)):
		if s[i] == "#":
			res += (i-leftmost)
	return res

pc = []
	
def iterate(inp, gens):
	print("{0:4} {1}".format(countpots(inp), inp))
	for i in range(gens):
		if i % 10000 == 0:
			print(i)
		inp = generate(inp)
		r = calcsumpots(inp, leftmost)
#		pc.append(r)
		#print(i, r)
		#print("{0:4} {2:5} {1}".format(countpots(inp), inp[:80], calcsumpots(inp, leftmost)))
	print(calcsumpots(inp, leftmost))

def test(s, offset, exp):
	r = calcsumpots(s, offset)
	if r == exp:
		res = " ++ "
	else:
		res = " -- "
	print("{4} got: {0} exp {1} (in: {2}/{3})".format(r, exp, s, offset, res))

def runtests():
	test("#", 0, 0)
	test("##", 1, -1)
	test("###", 1, 0)
	test("####", 1, 2)
	test("####", 0, 6)
	#test("####", -1, 1)



iterate(inp, 500000)

#for i in range(len(pc)-1):
#	print(i+1, pc[i], pc[i+1] - pc[i])

t = 50000000000
print(t, 5302 + (t-159)*33)


# not 2212


