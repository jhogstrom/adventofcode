import os
from timer import timeit

dataname = "dec3.txt"
# dataname = "dec3_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]



@timeit
def star1(data):
    wordlen = len(data[0])
    bitcount = [0] * wordlen

    for d in data:
        for i in range(wordlen):
            if d[i] == "1":
                bitcount[i] += 1

    gamma, epsilon  = "", ""
    for b in bitcount:
        if b > len(data)/2:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    # print(gamma, epsilon, gamma * epsilon)
    print(gamma * epsilon)


def onecount(numbers, p) -> int:
    return sum(1 for _ in numbers if _[p] == "1")


def filterdata(numbers, p, bit):
    return [_ for _ in numbers if _[p] == bit]


bitmap = { True: "1", False: "0"}

@timeit
def star2(data):
    scrubdata = [*data]
    wordlen = len(data[0])

    for i in range(wordlen):
        if len(data) > 1:
            data = filterdata(data, i, bitmap[onecount(data, i) >= len(data)/2])

        if len(scrubdata) > 1:
            scrubdata = filterdata(scrubdata, i, bitmap[onecount(scrubdata, i) < len(scrubdata)/2])

    generator = int(data[0], 2)
    scrub = int(scrubdata[0], 2)

    # print(generator, scrub, generator * scrub)
    print(generator * scrub)


star1(data)
star2(data)