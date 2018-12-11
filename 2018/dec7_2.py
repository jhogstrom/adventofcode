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
#@total_ordering
class Node:
	def __init__(self, graph, name):
		self.name = name
		self.done = False
		self.nextnodes = []
		self.graph = graph
		self.dependson = []
	def addnext(self, nextname):
		n = self.graph.findnode(nextname)
		n.dependson.append(self)
		self.nextnodes.append(n)
	def markdone(self):
		print("Did", self.name)
		self.done = True
	def depsdone(self):
		res = True
		for n in self.dependson:
			res &= n.done
		return res
	def __eq__(self, other):
		return self.name.lower() == other.name.lower()
	def __lt__(self, other):
		return self.name.lower() < other.name.lower()		
	def __hash__(self):
		return hash(self.name)
	def startexecute(self):
		r = ""#self.name
#		self.markdone()
		available = self.graph.getfirst()
		while available != []:
			n = available[0]
			if not n.name in r:
				r += n.name
			eligble = []
			n.markdone()
			for e in n.nextnodes:
				print("Checking", e.name, [_.name for _ in e.dependson])
				if e.depsdone():
					eligble.append(e)
			available = sorted(available[1:] + eligble)
			print([_.name for _ in available])
		return r

class Graph:
	def __init__(self):
		self.nodes = []

	def findnode(self, name):
		for n in self.nodes:
			if n.name == name:
				return n
		n = Node(self, name)
		#print("Creating ", name)
		self.nodes.append(n)
		return n
	def getfirst(self):
		res = []
		for n in self.nodes:
			if n.dependson == []:
				res.append(n)
		return res
	def reset(self):
		for n in self.nodes:
			n.done = False


#all = testdata

graph = Graph()

def readtree():
	for s in all:
		dofirst, thendo = [_.strip() for _ in s.split()][1::6]
		n = graph.findnode(dofirst)
		n.addnext(thendo)


readtree()
first = sorted(graph.getfirst())
#print(first.name)
print(first[0].startexecute())

#for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#	print(c, graph.findnode(c).startexecute())
#	graph.reset()
exit()
def getdeps(target):
	res = []
	for p in tree:
		if target in tree[p]:
			res.append(p)
	return sorted(res)

def getalltargets():
	return sorted(dobefore.keys())

def firsttarget():
	for c in doafter.keys():
		if not c in dobefore.keys():
			return c
def getpossible(donelist):
	print("Done", donelist)
	res = set()
	for d in donelist:
		for n in doafter[d]:
			if n in donelist:
				res.add(n)
	return sorted(list(res))


readtree()
t = getalltargets()
print(t)
print(sorted(doafter.keys()))


first = firsttarget()
done = []
done.append(first)
done += sorted(doafter[first])

donext = getpossible(done)

print("next:", donext)

print(first)
print(done)
exit()

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

#nopt BLMPUWX