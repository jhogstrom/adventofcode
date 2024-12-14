import logging
from typing import List, Tuple

from reader import get_data, set_logging, timeit

runtest = False
stardate = "13"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


class Machine:
    def __init__(
        self,
        a: Tuple[str, str],
        b: Tuple[str, str],
        target: Tuple[str, str],
        k: int = 0,
    ):
        self.ka = (int(a[0].split("+")[1]), int(a[1].split("+")[1]))
        self.kb = (int(b[0].split("+")[1]), int(b[1].split("+")[1]))
        self.target = (
            int(target[0].split("=")[1]) + k,
            int(target[1].split("=")[1]) + k,
        )

    def __str__(self):
        return "\n".join([f"A: {self.ka}", f"B: {self.kb}", f"Target: {self.target}"])

    def brute_solve(self) -> int:
        target = self.target
        ka = self.ka
        kb = self.kb
        for a in range(100):
            for b in range(100):

                if (
                    a * ka[0] + b * kb[0] == target[0]
                    and a * ka[1] + b * kb[1] == target[1]
                ):
                    return a * 3 + b
        return 0

    def solve(self) -> int:
        t = self.target
        a = self.ka
        b = self.kb

        B = (t[1] * a[0] - a[1] * t[0]) / (b[1] * a[0] - a[1] * b[0])
        A = (t[0] - B * b[0]) / a[0]

        if A != int(A) or B != int(B):
            return 0

        return int(A * 3 + B)


def parse_lines(lines: List[str], k: int = 0) -> Machine:
    A = lines[0].split(":")[1]
    B = lines[1].split(":")[1]
    prize = lines[2].split(":")[1]
    return Machine(A.split(","), B.split(","), prize.split(","), k)


def parse_machines(data, k: int = 0) -> List[Machine]:
    result = []
    i = 0
    while i < len(data):
        result.append(parse_lines(data[i : i + 3], k))  # noqa E203
        i += 4
    return result


@timeit
def star1(data):
    logging.debug("running star 1")
    machines = parse_machines(data)
    result = sum(m.solve() for m in machines)
    print(result)


@timeit
def star2(data):
    logging.debug("running star 2")
    machines = parse_machines(data, 10000000000000)
    result = sum(m.solve() for m in machines)
    print(result)


star1(data)
star2(data2)
