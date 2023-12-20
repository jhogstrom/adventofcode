from collections import deque
import logging
from math import prod
from pprint import pprint
from reader import get_data, timeit, set_logging

runtest = False
stardate = "19"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]

compare = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
}


class Comparison:
    def __init__(self, var, operator, value, target) -> None:
        self.var = var
        self.operator = operator
        self.value = value
        self.target = target

    def matches(self, part):
        if self.var not in part:
            return False
        return compare[self.operator](part[self.var], self.value)

    def __repr__(self) -> str:
        return f"{self.var}{self.operator}{self.value}:{self.target}"


class Workflow:
    def __init__(self, name, s) -> None:
        self.s = s
        self.name = name
        rules = s.split(",")
        self.rules = []
        for r in rules[:-1]:
            check, target = r.split(":")
            var = check[0]
            operator = check[1]
            value = int(check[2:])
            self.rules.append(Comparison(var, operator, value, target))
        self.default = rules[-1]

    def evaluate(self, part):
        for rule in self.rules:
            if rule.matches(part):
                return rule.target
        return self.default

    def __repr__(self) -> str:
        return self.s


def extract_workflows(data) -> dict[str, Workflow]:
    result = {}
    for line in data:
        if not line:
            break
        name, flow = line.split("{")
        result[name] = Workflow(name, flow[:-1])
    return result


def extract_parts(data):
    parts = []
    skip = True
    for line in data:
        if not line:
            skip = False
            continue
        if skip:
            continue
        part = {}
        for p in line[1:-1].split(","):
            part[p.split("=")[0]] = int(p.split("=")[1])
        parts.append(part)
    return parts


def apply_workflows(workflows: dict[str, Workflow], part):
    workflow_name = "in"
    while workflow_name not in ["R", "A"]:
        workflow_name = workflows[workflow_name].evaluate(part)
    return workflow_name


@timeit
def star1(data):
    logging.debug("running star 1")
    workflows = extract_workflows(data)
    parts = extract_parts(data)
    res = 0
    for part in parts:
        r = apply_workflows(workflows, part)
        if r == "A":
            res += sum(part.values())
    print(res)


def split_range(r, c, v, gt):
    cpy = r.copy()
    if gt:
        cpy[c] = (r[c][0], v)
        r[c] = (v+1, r[c][1])
    else:
        cpy[c] = (v, r[c][1])
        r[c] = (r[c][0], v-1)
    return [r, cpy]


@timeit
def star2(data):
    logging.debug("running star 2")
    r = {
        "x":  (1, 4000),
        "m":  (1, 4000),
        "a":  (1, 4000),
        "s":  (1, 4000),
    }

    workflows = extract_workflows(data)
    q = deque()
    q.append((r, "in"))
    endstates = {"A": [], "R": []}
    while len(q):
        r, workflow = q.pop()
        # print(f"** {workflow}")
        if workflow in endstates:
            endstates[workflow].append(r)
            continue
        for rule in workflows[workflow].rules:
            newr = split_range(r, rule.var, rule.value, rule.operator == ">")
            # print(rule)
            # pprint(newr)
            q.append((newr[0], rule.target))
            r = newr[1]
        q.append((r, workflows[workflow].default))
    res = sum(prod([v[1] - v[0] + 1 for v in _.values()]) for _ in endstates["A"])
    print(res)


star1(data)
star2(data2)


# in{s<1351:px,qqz}
# px{a<2006:qkq,m>2090:A,rfg} => s < 1351 && m > 2090: A
# qqz{s>2770:qs,m<1801:hdj,R} => s > 1351 && s < 2770 && m > 1801: R
# qkq{x<1416:A,crn} => s
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# crn{x>2662:A,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}