class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

class CircList:
    def __init__(self):
        self.current = None
        self.count = 0
        self.index = {}

    def insert(self, node):
        self.index[node.value] = node
        self.count += 1
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
        self.count -= 1
        c = self.current
        if self.current == None:
            return
        self.index[c.value] = None
        self.current.next.prev = self.current.prev
        self.current.prev.next = self.current.next
        self.current = self.current.next
        return c

    def popnext(self):
        self.count -= 1
        c = self.current.next
        self.current.next = self.current.next.next
        self.current.next.prev = self.current
        self.index[c.value] = None

        if c == self.first:
            self.first = self.current
        return c

    def move(self, p):
        if p > 0:
            for i in range(p):
                self.current = self.current.next
            return
        for i in range(abs(p)):
            self.current = self.current.prev

    def values(self):
        start = self.current
        res = [start.value]
        self.move(1)
        while self.current != start:
            res.append(self.current.value)
            self.move(1)
        return res

    def print(self):
        r = []
        c = self.first

        if c == self.current:
            r.append(f"({c.value})")
        else:
            r.append(f"{c.value}")
        c = c.next
        while c != self.first:
            if c == self.current:
                r.append(f"({c.value})")
            else:
                r.append(f"{c.value}")
            c = c.next
        print("  ".join(r))

data = "394618527"
# data = "389125467"

def parse(start_data):
    buff = CircList()
    for d in start_data:
        buff.insert(Node(int(d)))
    buff.move(1)
    return buff

def cycle(buff):
    # print("cups: ", end="")
    # buff.print()
    removedval = []
    for i in range(3):
        c = buff.popnext()
        removedval.append(c.value)
    # print(f"pick up: {', '.join([str(_) for _ in removed])}")

    dest = buff.current.value - 1
    if dest == 0:
        dest = buff.count + 3
    while dest in removedval:
        dest -= 1
        if dest == 0:
            dest = buff.count + 3
    # print(f"destination: {dest}")
    currp = buff.current

    buff.current = buff.index[dest]

    for n in removedval:
        buff.insert(Node(n))

    buff.current = currp
    buff.move(1)
    # print("==cycle done==")
    # print()


def star1():
    buff = parse(data)
    for i in range(100):
        cycle(buff)

    while buff.current.value != 1:
        buff.move(1)

    buff.move(1)
    res = []
    while buff.current.value != 1:
        res.append(str(buff.current.value))
        buff.move(1)
    return "".join(res)

def star2():
    buff = CircList()
    buff = parse(data)
    buff.move(-1)
    buff.print()
    print(data)
    for i in range(len(data), 1_000_000):
        buff.insert(Node(i+1))

    buff.move(1)

    for i in range(10_000_000):
        cycle(buff)
        if i % 100_000 == 0:
            print(i)

    buff.current = buff.index[1]

    print(f"Found 1: {buff.current.value}")
    buff.move(1)
    print(f"Next: {buff.current.value}")
    res = buff.current.value

    buff.move(1)
    print(f"Next: {buff.current.value}")
    res *= buff.current.value
    return res


print(f"* {star1()}")
print(f"* {star2()}")
