import logging
from collections import defaultdict, deque  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "24"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


class Pin:
    def __init__(self, name: str, value: int = None):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"


class Operation:
    def __init__(self, op, p1, p2, output):
        self.op = op
        self.input = [p1, p2]
        self.value = None
        self.output = output
        self.evaluated = False

    def __str__(self):
        return (
            f"{self.input[0].name} {self.op} {self.input[1].name} -> {self.output.name}"
        )

    def evaluate(self) -> None:
        self.evaluated = True
        if self.op == "XOR":
            self.value = self.input[0].value ^ self.input[1].value
        elif self.op == "AND":
            self.value = self.input[0].value & self.input[1].value
        elif self.op == "OR":
            self.value = self.input[0].value | self.input[1].value
        else:
            raise ValueError(f"Invalid operation {self.op}")
        self.output.value = self.value


def parse_data(data):
    pins = {}
    operations = []
    i = 0
    while i < len(data):
        line = data[i]
        if not line:
            break
        pin, value = line.split(":")
        value = int(value.strip())
        pins[pin] = Pin(pin, value)
        i += 1

    i += 1
    while i < len(data):
        line = data[i]
        p1, op, p2, _, output = line.split()
        if p1 not in pins:
            pins[p1] = Pin(p1)
        if p2 not in pins:
            pins[p2] = Pin(p2)
        if output not in pins:
            pins[output] = Pin(output)
        op = Operation(op, pins[p1], pins[p2], pins[output])
        operations.append(op)
        i += 1
    return pins, operations


@timeit
def star1(data):
    logging.debug("running star 1")
    pins, ops = parse_data(data)

    can_evaluate = [
        o for o in ops if all(p.value is not None for p in o.input) and not o.evaluated
    ]
    while can_evaluate:
        for op in can_evaluate:
            op.evaluate()
        can_evaluate = [
            o
            for o in ops
            if all(p.value is not None for p in o.input) and not o.evaluated
        ]

    r = 0
    outputs = [_ for _ in pins.values() if _.name.startswith("z")]
    for i, o in enumerate(sorted(outputs, key=lambda x: x.name)):
        r += o.value * 2**i
    print(r)

    # for o in ops:
    #     if all(_.value is not None for _ in o.input):
    #         print(o)


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
