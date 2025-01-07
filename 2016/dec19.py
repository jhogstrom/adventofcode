import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "19"
year = "2016"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"{self.value} -> {self.next.value}"


class Circle:
    def __init__(self, count):
        self.current = Node(1)
        self.current.next = self.current
        self.current.prev = self.current
        self.opposite = self.current
        self.count = 1
        self.last = self.current
        for i in range(2, count + 1):
            # print(f"adding {i}")
            node = Node(i)
            self.last.next.prev = node
            node.next = self.last.next
            self.last.next = node
            node.prev = self.last
            self.last = node
            self.count += 1
            if self.count % 2 == 0:
                self.opposite = self.opposite.next

    def __repr__(self):
        return f"{self.count} - {self.current} <-> {self.opposite}"

    def take_turn(self):
        self.current = self.current.next
        remove_node = self.opposite
        self.opposite = self.opposite.next
        self.count -= 1
        remove_node.prev.next = remove_node.next
        remove_node.next.prev = remove_node.prev
        if self.count % 2 == 0:
            self.opposite = self.opposite.next

    def print(self):
        node = self.current
        print(">>>", end=" ")
        for _ in range(self.count):
            if node == self.current:
                print(f"({node.value})", end=" ")
            elif node == self.opposite:
                print(f"[{node.value}]", end=" ")
            else:
                print(node.value, end=" ")
            node = node.next
        print()


@timeit
def star2(data):
    logging.debug("running star 2")

    count = 50 if runtest else int(data[0])
    elves = Circle(count)
    print("Setup done")
    while elves.count > 1:
        elves.take_turn()
        # elves.print()
        if elves.count % 1000 == 0:
            print(elves.count, end="\r")
    print(elves.current.value)


star1(data)
star2(data2)
