import os
from timer import timeit
from collections import defaultdict, deque

stardate = 16
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_jonne.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Node:
    def eat(self, c):
        v = int(self.s[:c], 2)
        self.s = self.s[c:]
        self.consumed += c
        return v

    def parse_value(self):
        endbit = self.eat(1)
        v = self.eat(4)
        val = bin(v)[2:].zfill(4)
        while endbit and len(self.s) > 4:
            # print(f"Number chunking: '{self.s}'")
            endbit = self.eat(1)
            v = self.eat(4)
            val += bin(v)[2:].zfill(4)
        # print(f"value: {int(val, 2)}")
        return int(val, 2)

    def version_sum(self):
        return self.version + sum(_.version_sum() for _ in self.children)

    def __str__(self) -> str:
        return f"Version: {self.version} Type {self.typeid} VSum: {self.version_sum()}"

    def __init__(self, s, level=0) -> None:
        self.s = s
        self.consumed = 0
        self.children = []

        self.version = self.eat(3)
        self.typeid = self.eat(3)
        print(" " * level, self.version, self.typeid, f"({level})")
        if self.typeid == 4:
            self.value = self.parse_value()
        else:
            length_id = self.eat(1)
            if length_id == 0: # eat a bit sequence
                payload_len = self.eat(15)
                eaten = 0
                payload = self.s[:payload_len]
                while eaten < payload_len:
                    n = Node(payload, level+1)
                    self.children.append(n)
                    eaten += n.consumed
                    payload = payload[n.consumed:]
                self.eat(payload_len)
            else: # eat n sub packages
                subpackages = self.eat(11)
                while len(self.children) != subpackages:
                    n = Node(self.s, level+1)
                    self.children.append(n)
                    self.eat(n.consumed)

    def calc_value(self):
        child_values = [_.calc_value() for _ in self.children]
        if self.typeid == 0:
            return sum(child_values)
        if self.typeid == 1:
            res = child_values[0]
            for _ in child_values[1:]:
                res *= _
            return res
        if self.typeid == 2:
            return min(child_values)
        if self.typeid == 3:
            return max(child_values)
        if self.typeid == 4:
            return self.value
        if self.typeid == 5:
            return 1 if child_values[0] > child_values[1] else 0
        if self.typeid == 6:
            return 1 if child_values[0] < child_values[1] else 0
        if self.typeid == 7:
            return 1 if child_values[0] == child_values[1] else 0


def print_tree(n: Node, level=0):
    tabs = " " * level
    print(tabs, n.typeid, n.version)
    for s in n.children:
        print_tree(s, level+1)


@timeit
def star1(data):
    binary = bin(int(data, 16))[2:]
    while len(binary) % 4:
        binary = "0" + binary
    c = 0
    while data[c] == "0":
        binary = "0000" + binary
        c += 1

    print(f"{data} => {binary}")
    n = Node(binary)
    print(str(n))
    print(n.calc_value())


star1(data[0])
