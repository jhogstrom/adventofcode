from timing import timeit
from buffers import SingleLinkedCircularBuffer as CircBuff, SingleNode as Node

data = "394618527"
data = "389125467"

def parse(start_data):
    buff = CircBuff()
    for d in start_data:
        buff.insert(Node(int(d)))
    buff.move(1)
    return buff

def cycle(buff):
    # print("cups: ", end="")
    # buff.print()
    dest = buff.current.value
    removedval = [dest]
    for i in range(3):
        removedval.append(buff.popnext().value)
    # print(f"pick up: {', '.join([str(_) for _ in removedval[1:]])}")

    while dest in removedval:
        dest -= 1
        if dest == 0:
            dest = buff.count + 3
    # print(f"destination: {dest}")
    currp = buff.current

    buff.current = buff.index[dest]
    for n in removedval[1:]:
        buff.insert(Node(n))

    buff.current = currp
    buff.move(1)
    # print("==cycle done==")
    # print()


def star1():
    buff = parse(data)

    for i in range(100):
        cycle(buff)

    while buff.current.value != 1:
        buff.move(1)

    buff.move(1)
    res = []
    while buff.current.value != 1:
        res.append(str(buff.current.value))
        buff.move(1)
    return "".join(res)

@timeit
def star2():
    buff = CircBuff()
    for d in data:
        buff.insert(Node(int(d)))
    for i in range(len(data), 1_000_000):
        buff.insert(Node(i+1))

    buff.move(1)

    for i in range(10_000_000):
        cycle(buff)
        if i % 100_000 == 0:
            print(i)

    buff.current = buff.index[1]

    print(f"Found 1: {buff.current.value}")
    buff.move(1)
    print(f"Next: {buff.current.value}")
    res = buff.current.value

    buff.move(1)
    print(f"Next: {buff.current.value}")
    res *= buff.current.value
    return res


print(f"* {star1()}")
print(f"* {star2()}")
