from collections import defaultdict
import os
import re
from typing import List
import logging

logging.basicConfig(level=logging.INFO)



runtest = True
stardate = 19
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()

material = {
    "geode": 0,
    "obsidian": 1,
    "clay": 2,
    "ore": 3
}


class Robot():
    def __init__(self, *, ore=0, clay=0, obsidian=0, material) -> None:
        self.cost = defaultdict(int)
        self.cost["obsidian"] = obsidian
        self.cost["clay"] = clay
        self.cost["ore"] = ore
        self.material = material

    def __str__(self) -> str:
        s = []
        for m, c in self.cost.items():
            if c > 0:
                s.append(f"{m}: {c}")
        return " ".join(s)

    def copy(self):
        return Robot(
            material=self.material,
            ore=self.cost["ore"],
            clay=self.cost["clay"],
            obsidian=self.cost["obsidian"])

    def produce(self):
        return [self.material, 1]

    def can_buy(self, resources):
        res = all(self.cost[m] <= resources[m] for m in self.cost)
        logging.debug(f"Can {'NOT' if not res else ''} buy {self.material}")
        return res

    def buy(self, resources):
        # print(f"\tBuying {self.material} robot")
        for m in resources:
            resources[m] -= self.cost[m]
        return self.copy()





class Blueprint():
    def __init__(self, values) -> None:
        self.num = values[0]
        self.robots = [
            Robot(material="geode", ore=values[5], obsidian=values[6]),
            Robot(material="obsidian", ore=values[3], clay=values[4]),
            Robot(material="clay", ore=values[2]),
            Robot(material="ore", ore=values[1])
        ]

    def max_cost(self, material):
        res = max(_.cost[material] for _ in self.robots)
        return res

    def is_needed(self, robot, robots):
        res = self.max_cost(robot.material) > robots[robot.material] or robot.material == "geode"
        logging.debug(f"Need to buy {robot.material} ({self.max_cost(robot.material)} > {robots[robot.material]}): {res}")
        return res


def parse_line(line):
    return Blueprint(list(map(int, re.findall(r'\d+', line))))


def best_result(result: List):
    best = None
    highest = 0
    for m in material:
        if best:
            return best
        for i, r in enumerate(result):
            if r is None:
                continue
            if r.get(m, 0) > highest:
                highest = r[m]
                best = r
    # if best:
    return best
    # raise ValueError(f"No best result found of {len(result)}")


MAXTIME = 24


def make_product(
        remaining: int,
        robots,
        produce,
        blueprint: Blueprint):
    # Time's up, go home
    if remaining == 0: # or produce is None:
        return produce

    m = MAXTIME-remaining+1
    if m < 15:
        logging.info(f"Minute {m} (Produced {list(produce.values())} -- Robots: {list(robots.values())}):")
    # input()

    # Find things to do
    potential_acquisitions = []
    for robot in blueprint.robots:
        if robot.can_buy(produce) and blueprint.is_needed(robot, robots):
            potential_acquisitions.append(robot)
    logging.debug(f"Potential acquisistions: {[_.material for _ in potential_acquisitions]}")

    # produce stuff
    for m, c in robots.items():
        produce[m] += c

    # execute all paths
    res = []
    for r in potential_acquisitions + [None]:
        p = {**produce}
        newbots = {**robots}
        if r is not None:
            newbots[r.buy(p).material] += 1
        logging.debug(f"Checking what happens if buying {r.material if r else 'nothing'}")
        # input()
        res.append(make_product(remaining-1, newbots, p, blueprint))

    # return the best
    res = best_result(res)
    return res


def star1():
    blueprints = [parse_line(_) for _ in data]
    res = 0
    for blueprint in blueprints:
        robots = {_: 0 for _ in material}
        robots["ore"] = 1
        produce = {_: 0 for _ in material}

        produce = make_product(MAXTIME, robots, produce, blueprint)

        logging.debug(f"\n{blueprint.num} - {produce.get('geode', 0)} => {blueprint.num * produce.get('geode', 0)}")
        res += blueprint.num * produce.get("geode", 0)
        # break
    return res


print("star1:", star1())
