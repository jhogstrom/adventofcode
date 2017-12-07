class Node:
    def __init__(self, s):
        parts = s.split(" ")
        self.name = parts[0]
        self.weight = int(parts[1][1:-1])
        self.childrennames = []
        self.children = []
        self.parent = None
        if len(parts) > 2:
            self.childrennames = [p.strip(",") for p in parts[3:]]
    def setparent(self, p):
        self.parent = p
        p.children.append(self)

    def childcount(self):
        return len(self.childrennames)

    def childweight(self):
        if self.childcount() == 0:
            return self.weight
        return sum(c.childweight() for c in self.children)

    def childrenbalanced(self):
        w = [c.childweight for c in self.children]
        return max(w) == min(w)

    def totalweight(self):
        if self.childcount() == 0:
            return self.weight
        return self.weight + sum(c.totalweight() for c in self.children)

inp = [Node(l.strip()) for l in open('7.txt')]

print([n.childrennames for n in inp])

def getnode(name):
    for n in inp:
        if n.name == name:
            return n
    raise IndexError

for n in inp:
    for c in n.childrennames:
        getnode(c).setparent(n)

p = inp[0]
while p.parent != None:
    p = p.parent

print(p.name)
print([c.totalweight() for c in p.children])

def examineweight(n):
    cw = [c.totalweight() for c in n.children]

    if min(cw) != max(cw):
        print(n.name, n.weight, cw)
        exit()
    for c in n.children:
        examineweight(c)

#examineweight(p.children[3].children[1])

n = p.children[3].children[1].children[2]
print(n.weight, n.childrennames)
for c in n.children:
    print(n.totalweight())