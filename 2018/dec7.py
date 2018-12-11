from collections import defaultdict
all=[ s.strip() for s in open('7','r').readlines()]

testdata = [
"Step C must be finished before step A can begin.",
"Step C must be finished before step F can begin.",
"Step A must be finished before step B can begin.",
"Step A must be finished before step D can begin.",
"Step B must be finished before step E can begin.",
"Step D must be finished before step E can begin.",
"Step F must be finished before step E can begin."
]

#all = testdata
deps = dict()
tree = defaultdict(list)
prereqtree = defaultdict(list)

def insertionnode(g, t):
	if g in t.keys():
		return t
	for n in t.values():
		return insertionnode(g, t[n])
	return None


def readtree():
	for s in all:
		goal, prereq = [_.strip() for _ in s.split()][1::6]
		#print(prereq, ":", goal)
		tree[goal].append(prereq)
		prereqtree[prereq].append(goal)

	print(tree.keys())
	for c in tree:
		print(c, "=>", tree[c])
	for c in prereqtree:
		print(c, "<=", prereqtree[c])

#	print(tree)

def getdeps(target):
	res = []
	for p in tree:
		if target in tree[p]:
			res.append(p)
	return sorted(res)

readtree()
alltargets = set()
for c in tree:
	for p in tree[c]:
		alltargets.add(p)

#print("all targets", alltargets)

#for c in sorted(alltargets):
#	print(c, "=>", getdeps(c))

def firsttarget():
	for c in tree:
		if not c in alltargets:
			return c

first = firsttarget()

def getnext(t):
	if not t in tree:
		return []
	return sorted(tree[t])

available = getnext(first)
#print(first, available)

#for n in next:
#	print(n, "=> ", getnext(n))

#for n in prereqtree:#
#	print(n, "=>", prereqtree[n]) 

#print(getnext("L"))
done = [first]
print("start with", first)
print(first, tree[first], available)
print(getnext(available[0]))
exit()
while available != []:
	n = available[0]
	done += n
	available = set()
	for d in done:
		for a in tree[d]:
			if a in done and a != d:
				available.add(a)
	available = sorted(list(available))
	print(done, available)

#	exit()
#
#
#	available = available[1:]
#	nextup = getnext(n)
#	print("Next downstream for {0}: {1}".format(n, nextup))
#	for t in nextup:
#		isdone = True
#		for p in prereqtree[t]:
#			if not p in done:
#				isdone = False
#		if isdone:
#			available.append(t)
#			print("All prereqs of {0} ({1}) are done. Adding it".format(t, prereqtree[t]))
#	available += getnext(n)
#	available = sorted(available)
#	print("done:", done, "available", available)

r = ""
for i in done:
	r += i
print("RESULT", r)
