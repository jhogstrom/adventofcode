import os
from timer import timeit
from collections import defaultdict, deque

stardate = 14
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Node():
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


class LinkedList():
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, node: Node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def __str__(self) -> str:
        res = []
        n = self.head
        while n != self.tail.next:
            res.append(str(n.value))
            n = n.next

        return ", ".join(res)


def parse_data(data):
    template = data[0]
    pairs = data[2:]
    rules = {}
    for p in pairs:
        from_, to = p.split(" -> ")
        rules[from_] = to

    res = LinkedList()
    for c in template:
        n = Node(c)
        res.append(n)

    return res, rules


def make_gen(template, rules):
    current = template.head
    while current.next:
        pair = current.value + current.next.value
        if pair in rules:
            node = Node(rules[pair])
            node.next = current.next
            current.next = node
            template.length += 1
            current = node
        current = current.next

def get_counts(template):
    counts = defaultdict(int)
    c = template.head
    while c:
        counts[c.value] += 1
        c = c.next
    return counts


@timeit
def star1(template, rules):
    for g in range(10):
        make_gen(template, rules)

    counts = get_counts(template)
    print("diff", g+1, max(counts.values()) - min(counts.values()))


@timeit
def star2(template, rules):
    pairs = {}
    for p in rules:
        pairs[p] = 0
    c = template.head

    counts = defaultdict(int)
    while c.next:
        pairs[c.value + c.next.value] += 1
        counts[c.value] += 1
        c = c.next
    counts[c.value] += 1

    for g in range(40):
        nextgen = defaultdict(int)
        for p in pairs:
            counts[rules[p]] += pairs[p]
            nextgen[p[0] + rules[p]] += pairs[p]
            nextgen[rules[p] + p[1]] += pairs[p]
        pairs = {**nextgen}

    print("diff", g+1, max(counts.values()) - min(counts.values()))


# In retrospect, star1 could easily be solved by star2.
# Keeping star1 solution to show how the solution doesn't scale :)
star1(*parse_data(data))
star2(*parse_data(data))