import os

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec6.txt'
_orbits = [_.strip() for _ in open(filename, 'r').readlines()]

#_orbits = ["COM)B",
#            "B)C",
#            "C)D",
#            "D)E",
#            "E)F",
#            "B)G",
#            "G)H",
#            "D)I",
#            "E)J",
#            "J)K",
#            "K)L",
#            "K)YOU",
#            "I)SAN"]

class Node:
    def __init__(self, name, tree):
        #print(f"Creating {name}")
        self.name = name
        self.parent = None
        self.children = []
        self.parent_name = None
        self.children_names = []
        self.tree = tree
        self._count = None
        tree[name] = self

    def __str__(self):
        return f"{self.parent_name} <- {self.name} <- {self.children_names}"

    def add_child(self, n):
        if n not in self.children_names:
            self.children_names.append(n)
        if n in self.tree:
            self.tree[n].parent_name = self.name

    def set_parent(self, n):
        if n in self.tree:
            self.tree[n].add_child(self.name)

    def getparent(self):
        if not self.parent_name:
            return None
        return self.tree[self.parent_name]

def get_node(name, all_orbits):
    if name in all_orbits:
        return all_orbits[name]
    return Node(name, all_orbits)

def scan_orbits(orbits):
    all_orbits = dict()
    for o in orbits:
        inner, outer = o.split(")")
        n = get_node(inner, all_orbits)
        n.add_child(outer)
        n = get_node(outer, all_orbits)
        n.set_parent(inner)

    for o in all_orbits:
        print(o, all_orbits[o].children_names)

    return all_orbits

def count_orbs(node):
    if not node.getparent():
        return 0
    return 1 + count_orbs(node.getparent())


def count_orbits(orbs):
    res = 0
    for node in orbs.values():
            res += count_orbs(node)           
    return res
        

orbs = scan_orbits(_orbits)

def star1():
    r = count_orbits(orbs)
    print(f"{r} - 1768 is too low")


def get_path(node):
    res = []
    while node.getparent():
        node = node.getparent()
        res.append(node.name)
    return res

def get_common_node(p1, p2):
    for n in p1:
        if n in p2:
            return n
    return None

def star2():
    SAN = orbs["SAN"]
    YOU = orbs["YOU"]
    print(SAN, get_path(SAN))
    print(YOU, get_path(YOU))

    pSAN = get_path(SAN)
    pYOU = get_path(YOU)

    meeting = get_common_node(pSAN, pYOU)
    print(meeting, pSAN.index(meeting) + pYOU.index(meeting))

star2()