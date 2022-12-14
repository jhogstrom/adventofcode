from functools import reduce
import os
from typing import List

runtest = False
stardate = "11"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Monkey():
    def __init__(self, desc: List[str], reducer) -> None:
        self.num = int(desc[0][-2])
        self.items = [int(_) for _ in desc[1].split(":")[1].split(",")]
        op = desc[2].split(":")[1].split()
        self.op = op[-2]
        self.opvalue = op[-1]
        self.test = int(desc[3].split(":")[1].split()[-1])
        self.targets = {
            True: int(desc[4].split()[-1]),
            False: int(desc[5].split()[-1])
        }
        self.inspected = 0
        self.reducer = reducer

    def desc(self):
        res = []
        res.append(f"Monkey {self.num}")
        res.append(f"Items: {', '.join([str(_) for _ in self.items])}")
        res.append(f"Operation: {self.op} {self.opvalue}")
        res.append(f"Test: {self.test}")
        res.append(f"Targets: {self.targets}")
        return res

    def __str__(self) -> str:
        return "\n".join(self.desc())

    def evaluate_op(self, old):
        term = old if self.opvalue == "old" else int(self.opvalue)
        return old * term if self.op == "*" else old + term

    def calc_worry_level(self, item: int):
        item = self.evaluate_op(item)
        return self.reducer(item)

    def evaluate(self, worry_level: int) -> bool:
        return worry_level % self.test == 0

    def round(self, monkeys, p):
        for item in self.items:
            worry_level = self.calc_worry_level(item)
            monkeys[self.targets[self.evaluate(worry_level)]].items.append(worry_level % p)

        self.inspected += len(self.items)
        self.items = []


def solve(rounds: int, reducer):
    monkeys = {i//7: Monkey(data[i:i+6], reducer) for i in range(0, len(data), 7)}

    # for i in monkeys:  # NOSONAR
    #     print(i, monkeys[i].desc())

    all_test_values = reduce(lambda x, y: x * y, [_.test for _ in monkeys.values()])

    for _ in range(rounds):
        for m in monkeys:
            monkeys[m].round(monkeys, all_test_values)

    _ = sorted([_.inspected for _ in monkeys.values()], reverse=True)
    return _[0] * _[1]


def star1():
    return solve(20, lambda x: x // 3)


def star2():
    return solve(10_000, lambda x: x)


print("star1:", star1())
print("star2:", star2())
