import os
from timer import timeit

dataname = "dec3.txt"
# dataname = "dec3_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]



@timeit
def star1():
    wordlen = len(data[0])
    bitcount = [0] * wordlen
    print(bitcount)
    for d in data:
        for i in range(wordlen):
            if d[i] == "1":
                bitcount[i] += 1

    print(bitcount)

    print(len(data))
    gamma  = ""
    epsilon = ""
    for b in bitcount:
        if b > len(data)/2:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    print(gamma * epsilon)


def onecount(numbers, p) -> int:
    res = 0
    for d in numbers:
        if d[p] == "1":
            res += 1
    return res


def filterdata(numbers, p, bit):
    res = [_ for _ in numbers if _[p] == bit]
    return res


bitmap ={ True: "1", False: "0"}

@timeit
def star2(data):
    org = [*data]
    wordlen = len(data[0])
    bitcount = [0] * wordlen
    # print(bitcount)

    for i in range(wordlen):
        c = onecount(data, i)
        data = filterdata(data, i, bitmap[c >= len(data)/2])
        if len(data) == 1:
            break

    # print(data)
    generator = int(data[0], 2)

    data = [*org]
    for i in range(wordlen):
        c = onecount(data, i)
        data = filterdata(data, i, bitmap[c < len(data)/2])
        if len(data) == 1:
            break
    scrub = int(data[0], 2)

    print(generator, scrub, generator * scrub)


# star1()
star2(data)