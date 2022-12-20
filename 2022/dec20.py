import os
from buffers import DblLinkedCircularBuffer, DoubleNode

runtest = False
stardate = 20
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


def parse(data) -> DblLinkedCircularBuffer:
    res = DblLinkedCircularBuffer()
    [res.insert(DoubleNode(int(_))) for _ in data]
    res.move(1)
    return res


def relocate(buff: DblLinkedCircularBuffer, n: DoubleNode, offset):
    buff.current = n
    buff.pop(n)
    buff.move(offset(n))
    buff.insert(n)


def find_node(org):
    for _ in org:
        if _.value == 0:
            return _
    raise ValueError("0 not found")


def star1():
    buff = parse(data)
    org = buff.nodes()
    for n in org:
        relocate(buff, n, lambda x: x.value-1)

    n = find_node(org)
    buff.current = n
    res = 0
    for _ in range(1, 4):
        buff.move(1000)
        res += buff.current.value

    return res


def star2():
    key = 811589153
    buff = parse(data)
    org = buff.nodes()
    for _ in org:
        _.value *= key

    for _ in range(10):
        for n in org:
            relocate(buff, n, lambda x: (x.value % buff.count) - 1)

    n = find_node(org)
    buff.current = n
    res = 0

    for _ in range(1, 4):
        buff.move(1000)
        res += buff.current.value

    return res


print("star1:", star1())
print("star2:", star2())
