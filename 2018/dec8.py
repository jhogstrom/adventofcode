data=[s.strip() for s in open('8','r').readlines()]

#data = ["2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"]

all = [int(_) for _ in data[0].split()]

class Node:
	metadata = []
	subnodes = []
	_sum = -1
	def __init__(self, subnodes, metadata):
		#print("Adding metadata", metadata)
		self.metadata = metadata
		self.subnodes = subnodes
	def sublength(self):
		res = 2 + len(self.metadata)
		for n in self.subnodes:
			res += n.sublength()
		return res

	def metadatasum(self):
		res = sum(self.metadata)
		for n in self.subnodes:
			res += n.metadatasum()
		return res

	def datalist(self):
		res = [len(self.subnodes), len(self.metadata)]
		for n in self.subnodes:
			res += n.datalist()
		for m in self.metadata:
			res.append(m)
		return res

	def asstring(self):
		r = ""
		for d in self.datalist():
			r += "{0} ".format(d)
		return r.strip()

	def star2sum(self):
		if self._sum != -1:
			return self._sum
		if len(self.subnodes) == 0:
			self._sum = self.metadatasum()
			return self._sum
		res = 0
		for m in self.metadata:
			i = m-1
			if i in range(len(self.subnodes)):
				res += self.subnodes[i].star2sum()
			self._sum = res
		return self._sum



def makenode(pos, n):
#	print("finding node {0} starting at {1}".format(n, pos))
	childcount = all[pos]
	metadatacount = all[pos+1]

	children = []
	
	for i in range(childcount):
		c = makenode(pos+2, n+1)
		children.append(c)

		pos += c.sublength()
	metadata = []
	for i in range(metadatacount):
		metadata.append(all[pos + i + 2])

#	print("Returning node {0} with {1} children and metadata {2}".format(n, len(children), metadata))
	return Node(children, metadata)

#n = Node([Node([], [1, 2, 3])], [2, 2, 2])
n = makenode(0, 0)
#print(n.metadata)
#print("len", n.sublength())
print("sum", n.metadatasum())
print("sum*2", n.star2sum())
#print("asstring", n.asstring())





