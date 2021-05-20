class Node:
    def __init__(self, v):
        self.value = v

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

class DoubleNode(Node):
    def __init__(self, v):
        super().__init__(v)
        self.next = None
        self.prev = None

class SingleNode(Node):
    def __init__(self, v):
        super().__init__(v)
        self.next = None
        self.prev = None


class DblLinkedCircularBuffer:
    def __init__(self):
        self.current = None
        self.count = 0
        self.index = {}

    def insert(self, node: DoubleNode):
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

    def move(self, p: int):
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
            # print(r)
            # print(c, self.first)
            if c == self.current:
                r.append(f"({c.value})")
            else:
                r.append(f"{c.value}")
            c = c.next
        print("  ".join(r))

class SingleLinkedCircularBuffer:
    def __init__(self):
        self.current = None
        self.count = 0
        self.index = {}

    def insert(self, node: SingleNode):
        # print(f"inserting {node}")
        self.index[node.value] = node
        self.count += 1
        if self.current == None:
            self.current = node
            node.next = node
            self.first = node
            return
        node.next = self.current.next
        self.current.next = node
        self.current = node

    # def delete(self):
    #     c = self.current
    #     if self.current == None:
    #         return
    #     self.count -= 1
    #     self.index[c.value] = None
    #     self.current.next.prev = self.current.prev
    #     self.current.prev.next = self.current.next
    #     self.current = self.current.next
    #     return c

    def popnext(self):
        self.count -= 1
        # print(f"Current is {self.current}")

        c = self.current.next
        # print(f"Next is {c}")
        self.current.next = self.current.next.next
        self.index[c.value] = None

        if c == self.first:
            self.first = self.current
        return c

    def move(self, p):
        if p > 0:
            for i in range(p):
                self.current = self.current.next
            return
        raise ValueError("Cannot move backward")

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
            # print(r)
            # print(c, self.first)
            if c == self.current:
                r.append(f"({c.value})")
            else:
                r.append(f"{c.value}")
            c = c.next
        print("  ".join(r))
