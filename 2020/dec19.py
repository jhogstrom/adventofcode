import helpers
import re

extra = "_demo"
extra = ""
data = helpers.get_data(__file__, extra=extra)

data, messages = helpers.get_records(data)


class Rule():
    def __init__(self, s, n):
        self.raw = s
        self.n = n
        self.chained = "\"" not in s

        if not self.chained:
            self.match = s[1]
        else:
            self.groups = []
            matchingrules = s.split("|")
            for m in matchingrules:
                self.groups.append([int(_) for _ in m.split()])

    def __str__(self):
        if not self.chained:
            return f"{self.n:3} Match str: {self.match}"

        r = []
        for rules in self.groups:
            r.append(f"({', '.join([str(_) for _ in rules])})")

        return f"{self.n:3} Match rules: {' | '.join(r)}"


def parse(data):
    res = {}
    for s in data:
        n, r = s.split(": ")
        res[int(n)] = Rule(r, int(n))
    return res


# This worked for star1, but not very well for star 2...
# debug = False
# def log(s):
#     if debug:
#         print(s)
#
# def match(rule, s, pos=0):
#     consumed = 0
#     # log(f"Pos {pos} in  {s[pos:]} Rule: {rule}")
#     if not rule.chained:
#         # log(f"s: {s}/{pos} s[{pos}] = '{s[pos]}' == '{rule.match}' -> {rule.match == s[pos]}\n")
#         return pos < len(s) and rule.match == s[pos], 1
#     res = False
#     matches = []
#     # For each group of rules
#     for group in rule.groups:
#         # log(f"--Group {group}")
#         group_match = True
#         # Check if the rule matches the next char
#         eaten = 0
#         for ix, _r in enumerate(group):
#             log(f"--Rule {_r} -> {rules[_r]}")
#             log(f"  Starting from {pos} + {eaten} = {pos + eaten}")
#             rule_match, eat = match(rules[_r], s, pos + eaten)
#             # log(f"Consumed: {eat}")
#             eaten += eat
#             # The entire group matches if all rules match
#             group_match &= rule_match
#             if not rule_match:
#                 log(f"XX Rule {_r} broken, skipping the rest in {group}")
#                 break
#         log(f">>Group {group} match: {group_match}")
#         # We can stop after the first matching group
#         matches.append((group_match, eaten))
#         if group_match:
#             res = True
#             consumed = max([eaten, consumed])
#             log(f"This means we skip the rest of the groups in {rule.groups}")
#             break
#     if any([_[0] for _ in matches]):
#         return True, max([_[1] for _ in matches])
#     return False,  0


def regexp(rule):
    if not rule.chained:
        return rule.match
    groups = []
    for g in rule.groups:
        rules_regexp = ["("]
        for rule in g:
            rules_regexp.append(regexp(rules[rule]))
        rules_regexp.append(")")
        groups.append("".join(rules_regexp))
    return f"({'|'.join(groups)})"


def ismatch(m, n):
    r0 = f"^{r42}+{r42}{{{n}}}{r31}{{{n}}}$"
    p0 = re.compile(r0)
    return p0.match(m)

rules = parse(data)

r42 = regexp(rules[42])
r31 = regexp(rules[31])
r0 = f"^{r42}{{2}}{r31}$"
p0 = re.compile(r0)

r = len([_ for _ in messages if p0.match(_)])
print(f"* {r}")

r = len([m for m in messages if any([ismatch(m, i) for i in range(1, 10)])])
print(f"** {r}")
exit()

# c = 0
# for i, m in enumerate(messages):
#     r = match(rules[0], m)
#     print(f"{i:2}: {r} -- {m} len: {len(m)}")
#     if r[0] and r[1] == len(m):
#         c += 1

# print(c)
