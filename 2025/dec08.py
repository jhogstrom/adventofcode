import logging
import math
from typing import List, Set, Tuple  # noqa E401

from reader import get_data, set_logging, timeit

runtest = False
stardate = "08"
year = "2025"


set_logging(runtest)
data = get_data(stardate, year, runtest)


def square(x: int) -> int:
    return x * x


class coord:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other) -> float:
        return math.sqrt(
            square(self.x - other.x)
            + square(self.y - other.y)
            + square(self.z - other.z)
        )

    def __repr__(self):
        return f"coord({self.x}, {self.y}, {self.z})"


def make_bokes(data) -> List[coord]:
    boxes = []
    for line in data:
        parts = line.split(",")
        a = coord(int(parts[0]), int(parts[1]), int(parts[2]))
        boxes.append(a)
    return boxes


def calc_distances(boxes: List[coord]) -> dict[tuple[coord, coord], float]:
    distances: dict[tuple[coord, coord], float] = {}
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            d = boxes[i].distance(boxes[j])
            distances[(boxes[i], boxes[j])] = d
    return distances


@timeit
def star1(distances):
    logging.debug("running star 1")

    circuits: List[Set[coord]] = []
    maxcompare = 10 if runtest else 1000
    shortest_distances = sorted(distances.items(), key=lambda x: x[1])[:maxcompare]
    for pair, _ in shortest_distances:
        found_circuit = None
        for c in circuits:
            if pair[0] in c or pair[1] in c:
                c.update({pair[0], pair[1]})
                found_circuit = c
                for oc in circuits:
                    if oc != c and (pair[0] in oc or pair[1] in oc):
                        found_circuit.update(oc)
                        oc.clear()

        if not found_circuit:
            circuits.append({pair[0], pair[1]})

    circuit_sizes = sorted([len(c) for c in circuits], reverse=True)[:3]
    logging.info(f"star 1: {circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]}")


@timeit
def star2(distances):
    logging.debug("running star 2")

    circuits: List[Set[coord]] = []
    shortest_distances = sorted(distances.items(), key=lambda x: x[1])
    for pair, _ in shortest_distances:
        found_circuit = None
        for c in circuits:
            if pair[0] in c or pair[1] in c:
                c.update({pair[0], pair[1]})
                found_circuit = c
                for oc in circuits:
                    if oc != c and (pair[0] in oc or pair[1] in oc):
                        found_circuit.update(oc)
                        oc.clear()
                if len([c for c in circuits if c]) == 1 and len(found_circuit) == len(
                    boxes
                ):
                    logging.info(f"star 2: {pair[0].x * pair[1].x}")
                    return

        if not found_circuit:
            circuits.append({pair[0], pair[1]})
        circuits = [c for c in circuits if c]  # Clean up empty circuits

    assert False, "Should not reach here"


boxes = make_bokes(data)
distances = calc_distances(boxes)

star1(distances)
star2(distances)
