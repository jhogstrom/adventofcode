import os
from timer import timeit
from collections import defaultdict

stardate = 8
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]


@timeit
def star1(data):
    counter = defaultdict(int)
    for s in data:
        _, output = s.split("|")
        for o in output.split():
            x = o.strip()
            counter[len(x)] += 1

    print(sum([counter[2], counter[4], counter[3], counter[7]]))


def stringcontains(target, value):
    return set(target) & set(value) == set(target)

def commonsegments(target, value, commoncount) -> bool:
    return len(set(target) & set(value)) == commoncount

def mapdigit(s, signals):
    for k, v in signals.items():
        if set(v) == set(s):
            return str(k)
    raise KeyError

@timeit
def star2(data):
    res = 0
    for s in data:
        signals, output = s.split("|")
        output = [_.strip() for _ in output.split()]
        signals = [_.strip() for _ in signals.split()]

        signalmap = {}
        signalmap[1] = list(filter(lambda x: len(x) == 2, signals))[0]
        signals.remove(signalmap[1])
        signalmap[7] = list(filter(lambda x: len(x) == 3, signals))[0]
        signals.remove(signalmap[7])
        signalmap[4] = list(filter(lambda x: len(x) == 4, signals))[0]
        signals.remove(signalmap[4])
        signalmap[8] = list(filter(lambda x: len(x) == 7, signals))[0]
        signals.remove(signalmap[8])

        # The only 6 segment without seg C
        signalmap[6] = list(filter(lambda x: not stringcontains(signalmap[1], x), filter(lambda x: len(x) == 6, signals)))[0]
        signals.remove(signalmap[6])

        # The only 6 segment without seg D
        signalmap[0] = list(filter(lambda x: not stringcontains(signalmap[4], x), filter(lambda x: len(x) == 6, signals)))[0]
        signals.remove(signalmap[0])

        # The only remaining 6 segment...
        signalmap[9] = list(filter(lambda x: len(x) == 6, signals))[0]
        signals.remove(signalmap[9])

        # The only 5 segment with seg C & F
        signalmap[3] = list(filter(lambda x: stringcontains(signalmap[1], x), signals))[0]
        signals.remove(signalmap[3])

        # The only 5 segment with 3 segments common to 4
        signalmap[5] = list(filter(lambda x: commonsegments(signalmap[4], x, 3), signals))[0]
        signals.remove(signalmap[5])

        # Now only 2 remains...
        signalmap[2] = signals[0]
        signals.remove(signalmap[2])

        v = ""
        for d in output:
            v += mapdigit(d, signalmap)
        res += int(v)

    print(res)


star1(data)
star2(data)
