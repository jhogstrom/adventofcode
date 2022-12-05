from collections import defaultdict
import os

runtest = False
stardate = "05"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


def read_stacks():
    stacklines = []
    for _ in data:
        if _:
            stacklines.append(_)
        else:
            break
    return stacklines


def init_stacks(stacklines):
    stacks = defaultdict(list)
    for _ in stacklines[:-1]:
        _ = _.replace("    ", " _  ")
        piles = _.split()
        for i, p in enumerate(piles):
            if p != "_":
                stacks[i].append(p[1])
    for _ in stacks:
        stacks[_] = stacks[_][::-1]

    return stacks


def get_instructions():
    i = 1
    for _ in data:
        if _ == "":
            break
        i += 1
    return data[i:]


def print_stacks(stacks):
    msg = []

    m = ""
    largest = 0
    for _ in range(len(stacks)):
        m += f" {_+1}  "
        largest = max(largest, len(stacks[_]))
    msg.append(m)

    for s in range(largest):
        m = ""
        for _ in range(len(stacks)):
            if len(stacks[_]) > s:
                # print(s, stacks[_])
                m += f"[{stacks[_][s]}] "
            else:
                m += "    "
        msg.append(m)

    for _ in msg[::-1]:
        print(_)
    print("+++")


def execute(instruction, stacks):
    _, count, _, start, _, to = instruction.split()
    count = int(count)
    start = int(start) - 1
    to = int(to) - 1

    # print(instruction, "   [", count, start, to, "]")
    for _ in range(count):
        stacks[to].append(stacks[start].pop())
    # print_stacks(stacks)


def execute2(instruction, stacks):
    _, count, _, start, _, to = instruction.split()
    count = int(count)
    start = int(start) - 1
    to = int(to) - 1

    # print(instruction, "   [", count, start, to, "]")
    for _ in range(count):
        stacks[to].append(stacks[start][len(stacks[start]) - count + _])
    stacks[start] = stacks[start][:-count]
    # print_stacks(stacks)


def get_top_stacks(stacks):
    msg = ""
    for _ in range(len(stacks)):
        msg += stacks[_][-1]
    return msg


def star1():
    s = read_stacks()
    stacks = init_stacks(s)
    instructions = get_instructions()
    # print_stacks(stacks)

    for _ in instructions:
        execute(_, stacks)

    return get_top_stacks(stacks)


def star2():
    s = read_stacks()
    stacks = init_stacks(s)
    instructions = get_instructions()
    # print_stacks(stacks)

    for _ in instructions:
        execute2(_, stacks)

    return get_top_stacks(stacks)


print("star1:", star1())
print("star2:", star2())
