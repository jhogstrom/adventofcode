import os
from timer import timeit
from collections import defaultdict, deque
import itertools

stardate = 18
dataname = f"dec{stardate}.txt"
dataname = f"dec{stardate}_test.txt"
# dataname = f"dec{stardate}_ex0.txt"
# dataname = f"dec{stardate}_ex1.txt"
# dataname = f"dec{stardate}_ex2.txt"
# dataname = f"dec{stardate}_ex3.txt"
# dataname = f"dec{stardate}_ex4.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Node():
    def __init__(self, s: str, parent = None) -> None:
        self.parent = parent
        left = self.leftpart(s)
        if left == s:
            self.left = None
            self.right = None
            self.value = int(s)
            return
        right = s[len(left)+2:-1]
        self.left = Node(left, self)
        self.right = Node(right, self)

    def __str__(self) -> str:
        if hasattr(self, "value"):
            return str(self.value)
        return f"[{self.left},{self.right}]"

    @property
    def parent_count(self):
        res = 0
        p = self.parent
        while p:
            res += 1
            p = p.parent
        return res

    @property
    def child_count(self):
        if self.isleaf:
            return 1
        return self.left.child_count + self.right.child_count

    @property
    def root(self):
        p = self
        while p.parent:
            p = p.parent
        return p

    @property
    def isleaf(self):
        return hasattr(self, "value")

    def leftpart(self, s: str) -> str:
        lpar = []
        commas = []
        lastcomma = -1

        if "," not in s:
            return s
        for i, c in enumerate(s):
            if c == "[":
                lpar.append(i)
            if c == "]":
                lpar.pop()
                lastcomma = commas.pop()
            if c == ",":
                commas.append(i)
            if len(lpar) == 0 and lastcomma != -1:
                return s[1: lastcomma]

    @property
    def children(self):
        if hasattr(self, "value"):
            return [self]
        return [self] + self.left.children + self.right.children

    def get_left_value_node(self, caller=None):
        nodes = self.root.children
        i = nodes.index(self)
        i -= 1
        while i >= 0:
            if nodes[i].isleaf:
                return nodes[i]
            i -= 1
        return None

    @property
    def magnitude(self):
        if self.isleaf:
            return self.value
        else:
            return 3 * self.left.magnitude + 2 * self.right.magnitude

    def get_right_value_node(self, owner=None):
        nodes = self.root.children
        i = nodes.index(self) + 2
        i += 1
        while i < len(nodes):
            if nodes[i].isleaf:
                return nodes[i]
            i += 1
        return None

    def split(self):
        # print(f"Splitting {self}")
        left = int(self.value / 2)
        right = int(0.5 + self.value/2)
        delattr(self, "value")
        self.left = Node(str(left), self)
        self.right = Node(str(right), self)
        # print(f"ROOT (after split) : {self.root}")

    def explode(self):
        # print("EXPLODING", str(self))
        leftnode = self.get_left_value_node()
        rightnode = self.get_right_value_node()
        # print(f"Node values: left - {str(leftnode):>3} right - {str(rightnode):>3}")
        if leftnode:
            leftnode.value += self.left.value
        if rightnode:
            rightnode.value += self.right.value
        self.value = 0
        self.left = None
        self.right = None
        # print(f"new values : left - {str(leftnode):>3} right - {str(rightnode):>3}")
        # print(f"ROOT: {self.root}")

    def reduce(self):
        nodes = self.children
        for n in nodes:
            if n.parent_count == 4 and n.child_count == 2:
                n.explode()
                return True
        return False

    def dosplit(self):
        nodes = self.children
        for n in nodes:
            if n.isleaf and n.value >= 10:
                n.split()
                return

    def doreduce(self):
        s = "foobar"
        newstr = str(self)
        while s != newstr:
            s = newstr
            if not self.reduce():
                self.dosplit()
            newstr = str(self)

    def add(self, n):
        if self.parent or n.parent:
            raise ValueError("Can only add root nodes")

        node = Node("0")
        node.left = self
        self.parent = node

        node.right = n
        n.parent = node

        delattr(node, "value")
        return node

def test_explode(s, expected):
    n = Node(s)
    n.reduce()
    print(str(n))
    if str(n) == expected:
        print("PASSED")
    else:
        print(">>> FAILED")
        raise
    print("===")

def test_split(s, expected):
    n = Node(s)
    assert(s == str(n))
    n.dosplit()
    print(str(n))
    if str(n) == expected:
        print("PASSED")
    else:
        print(">>> FAILED")
        raise
    print("===")

def test_explodes():
    test_explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]" )
    test_explode("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
    test_explode("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
    test_explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

def test_splits():
    test_split("10", "[5,5]")
    test_split("11", "[5,6]")
    test_split("12", "[6,6]")

def test_magnitude(s, v):
    n = Node(s)
    assert(n.magnitude == v)

def test_magnitudes():
    test_magnitude("[9,1]", 29)
    test_magnitude("[1, 9]", 21)
    test_magnitude("[[1,2],[[3,4],5]]", 143)
    test_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)
    test_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)

@timeit
def star1(data):
    # test_explodes()
    # test_splits()
    # test_magnitudes()
    # exit()
    n = Node(data[0])
    # print(f"Starting with.: {n}")
    for s in data[1:]:
        n = n.add(Node(s))
        # print(f"After adding..: {n}")
        n.doreduce()
        # print(f"After reducing: {n}")
    print(n.magnitude)


@timeit
def star2(data):
    maxval = 0
    maxnode = None
    for pair in itertools.permutations(data, 2):
        n = Node(pair[0])
        n = n.add(Node(pair[1]))
        n.doreduce()
        # print(pair[0])
        # print(pair[1])
        # print(n.magnitude)
        # print("===")
        if n.magnitude > maxval:
            maxval = n.magnitude
            maxnode = n

    print(maxval)
    print(str(maxnode))

data2 = data[:]
star1(data)
star2(data2)