from collections import defaultdict
#452 players; last marble is worth 71250 points

players, marbles, hs = 452, 71250*100, -1

#players, marbles, hs = 9, 25, 32
#players, marbles, hs = 10, 1618, 8317
#players, marbles, hs = 13, 7999, 146373
#players, marbles, hs = 17, 1104, 2764
#players, marbles, hs = 21, 6111, 54718
#players, marbles, hs = 30, 5807, 37305

class Node:
	def __init__(self, v):
		self.value = v
		self.next = None
		self.prev = None

class CircList:
	def __init__(self):
		self.current = None

	def insert(self, node):
		if self.current == None:
			self.current = node
			node.next = node
			node.prev = node
			self.first = node
			return
		node.prev = self.current
		node.next = self.current.next
		node.next.prev = node
		node.prev.next = node
		self.current = node

	def delete(self):
		if self.current == None:
			return
		self.current.next.prev = self.current.prev
		self.current.prev.next = self.current.next
		self.current = self.current.next

	def move(self, p):
		if p > 0:
			for i in range(p):
				self.current = self.current.next
			return
		for i in range(abs(p)):
			self.current = self.current.prev

	def print(self):
		r = ""
		c = self.first
		if c == self.current:
			r += " ({0:2})".format(c.value)
		else:
			r += "  {0:2} ".format(c.value)
		c = c.next
		while c != self.first:
			if c == self.current:
				r += " ({0:2})".format(c.value)
			else:
				r += "  {0:2} ".format(c.value)
			c = c.next
		print(r)

l = CircList()
l.insert(Node(0))
l.print()

player = -1
score = defaultdict(int)
for i in range(1, marbles+1):
	if i % 10000 == 0:
		print(i)
	player = (player + 1) % (players)
	if i % 23 == 0:
		#print("mod 23! <=", i)
		score[player] += i
		l.move(-7)
		score[player] += l.current.value
		l.delete()
	else:
		l.move(1)
		l.insert(Node(i))
#	l.print()


print("high score=", max(score.values()))
print("Expected  =", hs)