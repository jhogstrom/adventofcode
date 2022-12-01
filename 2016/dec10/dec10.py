
from collections import defaultdict
from typing import List

class Rule:
    def __init__(self) -> None:
        s =

class Robot():
    def __init__(self, robots: List, rule: str) -> None:
        self.rule = rule
        self.chips = []
        self.robots = robots

    def accept_chip(self, chip: int):
        self.chips.append(chip)
        if len(self.chips == 2):
            self.apply_rule()



    def apply_rule(self):
        self.yield_low_chip()
        self.yield_high_chip()
        self.chips = []





def get_lines():
    with open("2016/dec10/dec10.txt") as f:
        return [_.strip() for _ in f.readlines()]


robots = defaultdict(list)

lines = get_lines()
nextlines = []
for _ in lines:
    tokens = _.split()
    if tokens[0] == "value":
        robots[tokens[-1]].append(int(tokens[1]))
    else:
        nextlines.append(_)

for _ in robots:
    print(_, robots[_])

print(robots['123'])

lines = nextlines[:]
nextlines = []
outputs = defaultdict(list)

while lines:
    for _ in lines:
        tokens = _.split()
        isbot = tokens[0] == "bot"
        if not isbot:
            continue
        bot = tokens[1]
        # print(bot)
        if len(robots[bot]) == 2:
            lowbot = tokens[6]
            highbot = tokens[-1]
            print(_)
            if tokens[5] == "bot":
                robots[lowbot].append(min(robots[bot]))
                # print(lowbot, robots[lowbot])
            else:
                outputs[lowbot].append(min(robots[bot]))
                # print("outputs", outputs)

            if tokens[10] == "bot":
                robots[highbot].append(max(robots[bot]))
                # print(highbot, robots[highbot])
            else:
                outputs[lowbot].append(min(robots[bot]))
                # print("outputs", outputs)
            if 61 in robots[bot] or 17 in robots[bot]:
                print("Movement", bot, robots[bot], _)
            robots[bot] = []
        else:
            nextlines.append(_)
    lines = nextlines[:]
    nextlines = []
    print("===")
    # input("[enter]")

for _, chips in robots.items():
    if 61 in chips or 17 in chips:
        print("answer", _)

