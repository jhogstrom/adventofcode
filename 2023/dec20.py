import logging
from collections import defaultdict, deque

from reader import get_data, set_logging, timeit

runtest = False
stardate = "20"
year = "2023"
testnum = "2"

set_logging(runtest)
data = get_data(stardate, year, runtest, testnum)


class Node:
    def __init__(self, s) -> None:
        self.signals = defaultdict(int)
        self.state = False
        name, dest = s.split(" -> ")
        self.name = name
        if name[0] in "%&":
            self.op = name[0]
            self.name = name[1:]
        else:
            self.op = None
        self.dests = dest.split(", ")
        self.inputs = {}

    def receive(self, sender: str, signal):
        res = None
        if not self.op:
            self.signals[signal] += len(self.dests)
            res = zip(
                [self.name] * len(self.dests), self.dests, [signal] * len(self.dests)
            )
        elif self.op == "%":
            if signal:
                res = []
            else:
                self.state = not self.state
                self.signals[self.state] += len(self.dests)
                res = zip(
                    [self.name] * len(self.dests),
                    self.dests,
                    [self.state] * len(self.dests),
                )
        elif self.op == "&":
            self.inputs[sender] = signal
            send_signal = any(not _ for _ in self.inputs.values())
            self.signals[send_signal] += len(self.dests)
            res = zip(
                [self.name] * len(self.dests),
                self.dests,
                [send_signal] * len(self.dests),
            )
        else:
            raise ValueError("Unknown op")
        res = list(res)
        # logging.debug(f"{self.name} ({self.op if self.op else ''}) received {signal} from {sender}  -> {res}")
        return res

    def __repr__(self) -> str:
        return f"{self.name} -> {self.dests}"


def parse_data(data):
    nodes = [Node(_) for _ in data]
    nodes = {_.name: _ for _ in nodes}
    # Set default input signals
    for n in nodes.values():
        for d in n.dests:
            dest = nodes.get(d)
            if dest and dest.op == "&":
                nodes[d].inputs[n.name] = False

    nodes["button"] = Node("button -> broadcaster")
    return nodes


@timeit
def star1(data):
    logging.debug("running star 1")
    nodes = parse_data(data)
    q = deque()
    BUTTONS = 1000
    for _ in range(BUTTONS):
        q.extend(nodes["button"].receive("start", False))
        while q:
            sender, receiver, signal = q.popleft()
            if receiver not in nodes:
                logging.debug(f"skipping {receiver}")
                continue
            res = nodes[receiver].receive(sender, signal)
            q.extend(res)

    lo, hi = 0, 0
    for _ in nodes:
        lo += nodes[_].signals[False]
        hi += nodes[_].signals[True]
    print(f"Lo: {lo}\nHi: {hi}\n\n{lo*hi}")


@timeit
def star2(data):
    logging.debug("running star 2")
    nodes = parse_data(data)
    q = deque()

    c = 0
    while True:
        c += 1
        q.extend(nodes["button"].receive("start", False))
        while q:
            sender, receiver, signal = q.popleft()
            if receiver == "rx" and not signal:
                print(c)
                exit()
            if receiver not in nodes:
                # logging.debug(f"skipping {receiver}")
                continue
            res = nodes[receiver].receive(sender, signal)
            q.extend(res)
        amps = [_ for _ in nodes if nodes[_].op == "&"]
        sigs = []
        for a in amps:
            s = "".join(["1" if _ else "0" for _ in sorted(nodes[a].inputs.values())])
            sigs.append(s)
        print(c, " - ".join(sigs))

        if c == 1000000:
            exit()


star1(data)
star2(data)
