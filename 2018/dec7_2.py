from collections import defaultdict
all=[ s.strip() for s in open('7','r').readlines()]

BASECOST=60

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
		self.cost = BASECOST + "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(name) + 1
		self.inprogress = False
	def startwork(self):
		self.inprogress = True
	def tick(self):
		self.cost -= 1
		if self.cost == 0:
			self.markdone()
	def addnext(self, nextname):
		n = self.graph.findnode(nextname)
		n.dependson.append(self)
		self.nextnodes.append(n)
	def markdone(self):
		#print("Did", self.name)
		self.inprogress = False
		self.done = True
	def depsdone(self):
		res = True
		for n in self.dependson:
			res &= n.done
		return res
	def __eq__(self, other):
		if other == None: return False
		return self.name.lower() == other.name.lower()
	def __lt__(self, other):
		return self.name.lower() < other.name.lower()		
	def __hash__(self):
		return hash(self.name)

class Graph:
	def __init__(self, w):
		self.nodes = []
		self.workers = [None for _ in range(w)]
		self.totaltime = 0
		self.completednodes = ""
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
		return sorted(res)
	def reset(self):
		for n in self.nodes:
			n.done = False
	def alldone(self):
		for n in self.nodes:
			if not n.done:
				return False
		return True

	def freeworker(self, node):
		if node in self.workers:
			return False
		for w in self.workers:
			if w == None:
				return True
		return False

	def assignwork(self, node):
		for i in range(len(self.workers)):
			if self.workers[i] == None:
				self.workers[i] = node
				node.startwork()
				return

	def tick(self):
		self.totaltime += 1
		for w in self.workers:
			if w != None:
				w.tick()

	def getcompleted(self):
		res = []
		for i in range(len(self.workers)):
			if self.workers[i] != None and self.workers[i].done:
				res.append(self.workers[i])
				self.workers[i] = None
		return res

	def completednodes_(self):
		res = []
		for n in self.nodes:
			if n.done:
				res.append(n.name)
		return "".join(sorted(res))

	def nodesinprogress(self):
		res = []
		for n in self.nodes:
			if n.inprogress:
				res.append(n.name)
		return "".join(sorted(res))		

	def printstatus(self):
		r = "{0:3} ".format(self.totaltime)
		for w in self.workers:
			if None == w:
				r += ". "
			else:
				r += w.name + " "
		r += " {0:{1}} ".format(self.completednodes, len(self.nodes))
		r += " [{0}]".format(self.nodesinprogress())
		print(r)

	def execute(self):
		available = self.getfirst()
		while not self.alldone():
			inprogress = []
			for n in available:
				if self.freeworker(n):
					self.assignwork(n)
					inprogress.append(n)

			for n in inprogress:
				available.remove(n)

			self.printstatus()

			self.tick()
			completed = self.getcompleted()

			newnodes = []
			for n in completed:
				self.completednodes += n.name
				newnodes += n.nextnodes
				#print("Completed", n.name, "possibly eligeble", [_.name for _ in n.nextnodes])
				#print("Total eligeble: ", [_.name for _ in newnodes])

			eligble = []

			for e in newnodes:
				#print("Checking", e.name, [_.name for _ in e.dependson])
				if e.depsdone():
					eligble.append(e)
					#print("+Found", e.name, "to do")
				else:
					#print("-", e.name, "is not ready")
					pass
			available = sorted(available + eligble)
			#print([_.name for _ in available])
		return self.completednodes

#all = testdata

graph = Graph(5)

def readtree():
	for s in all:
		dofirst, thendo = [_.strip() for _ in s.split()][1::6]
		n = graph.findnode(dofirst)
		n.addnext(thendo)


readtree()
print(graph.execute())
print(graph.totaltime)