import os
import itertools
from timing import timeit
import enum
from collections import defaultdict

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
# "class: 1-3 or 5-7",
# "row: 6-11 or 33-44",
# "seat: 13-40 or 45-50",
# "",
# "your ticket:",
# "7,1,14",
# "",
# "nearby tickets:",
# "7,3,47",
# "40,4,50",
# "55,2,20",
# "38,6,12",
# ]

# data = [
# "class: 0-1 or 4-19",
# "row: 0-5 or 8-19",
# "seat: 0-13 or 16-19",
# "",
# "your ticket:",
# "11,12,13",
# "",
# "nearby tickets:",
# "3,9,18",
# "15,1,5",
# "5,14,9",
# ]

class Rule:
    def __init__(self, s):
        self.name, ranges = s.split(": ")
        self.ranges = []

        for r in ranges.split(" or "):
            self.ranges.append([int(_) for _ in r.split("-")])

    def __str__(self):
        rstr = []
        for r in self.ranges:
            rstr.append('-'.join([str(_) for _ in r]))

        return f"{self.name}: {' or '.join(list(rstr))}"

    def __repr__(self):
        return str(self)

    def valid(self, n):
        return any([r[0] <= n <=r[1] for r in self.ranges])


def parse():
    scanmode = 0
    rules = []
    tickets = []
    for s in data:
        if s == "":
            continue
        if s == "your ticket:":
            scanmode += 1
            continue
        if s == "nearby tickets:":
            scanmode += 1
            continue
        if scanmode == 0:
            rules.append(Rule(s))
        elif scanmode == 1:
            myticket = [int(_) for _ in s.split(",")]
        else:
            tickets.append([int(_) for _ in s.split(",")])

    return rules, myticket, tickets

@timeit
def star1(rules, tickets):
    errors = []
    valid = []

    for t in tickets:
        isvalid = True
        for v in t:
            if not any([r.valid(v) for r in rules]):
                errors.append(v)
                isvalid = False
        if isvalid:
            valid.append(t)
    return sum(errors), valid

@timeit
def star2(rules, valid_tickets, myticket):
    matched_rules = []
    res = 1
    # Eliminate until all rules are matched.
    while len(matched_rules) != len(rules):
        # Temp map from index -> matching rules
        matching_rules = defaultdict(list)
        # Iterate over all numbers
        for ix in range(len(myticket)):
            # Get all the values on position ix
            all_values = [myticket[ix]] + [t[ix] for t in valid_tickets]

            # The matching rules are
            # * Not matched before
            # * Valid for all numbers on position x
            matching_rules[ix] = [r for r in rules \
                if \
                    r not in matched_rules \
                    and all([r.valid(_) for _ in all_values])]

        # Get the index and rule where only one rule matched the numbers
        ix, m = [(k, v[0]) for k, v in matching_rules.items() if len(v) == 1][0]

        # Don't check this rule again
        matched_rules.append(m)
        # If it matched the sought rules, multiply it  to the answer
        if "departure" in m.name:
            res *= myticket[ix]
    return res


rules, myticket, tickets = parse()

s1, valid = star1(rules, tickets)
print(f"* {s1}")
print(f"** {star2(rules, valid, myticket)}")

for s in data[-1::-1]:
