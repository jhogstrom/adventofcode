import os
import itertools
import time
from timing import timeit

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec7.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
#     "light red bags contain 1 bright white bag, 2 muted yellow bags.",
#     "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
#     "bright white bags contain 1 shiny gold bag.",
#     "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
#     "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
#     "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
#     "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
#     "faded blue bags contain no other bags.",
#     "dotted black bags contain no other bags."
#     ]

class Color():
    def __init__(self, s):
        parts = s.split()
        self.qty = int(parts[0])

        self.color = f"{parts[1]} {parts[2]}"

    def __str__(self):
        if self.qty == 0:
            return f"{self.qty} no other"

        return f"{self.qty} {self.color}"

class Rule():
    def __init__(self, s):
        self.containsrules = {}
        self.contains = []
        parts = s[:-1].split(" contain ")
        self.color = parts[0][:-5]
        if parts[1] == "no other bags":
            return

        contains = parts[1].split(", ")

        self.contains = [Color(_) for _ in contains]

    def __str__(self):
        containers = [str(_.color) for _ in self.containers]
        return f">{self.color}< -> {[str(_) for _ in self.contains]}"

    def cancontain(self, color):
        return color == self.color or any([_.cancontain(color) for _ in self.containsrules.values()])

    def mustcontain(self):
        return 1 + sum([c.qty * self.containsrules[c.color].mustcontain() for c in self.contains])

rules = []
@timeit
def parsedata():
    global rules
    rules = [Rule(_) for _ in data]

    for r in rules:
        for contains in r.contains:
            for _ in rules:
                if contains.color == _.color:
                    r.containsrules[_.color] = _

@timeit
def star1():
    count = 0
    for r in rules:
        if r.cancontain("shiny gold"):
            count += 1
    print(f"* {count-1}")

@timeit
def star2():
    rule = [_ for _ in rules if _.color == "shiny gold"][0]
    print(f"** {rule.mustcontain()-1}")


parsedata()
star1()
star2()