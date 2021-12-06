import os
from timer import timeit
from collections import defaultdict

stardate = 6
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
data = [int(_) for _ in data[0].split(",")]


class Node():
    def __init__(self, value) -> None:
        self.value = value
        self.next = None


class LinkedList():
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, node: Node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1
        # print(node.value)
        # print(self.head.value, self.head.next)

    def __str__(self) -> str:
        res = []
        n = self.head
        while n != self.tail.next:
            res.append(str(n.value))
            # print(n.value)
            n = n.next

        return ", ".join(res)


def star1(data):
    # print(len(data), "--", data)
    for day in range(256):
        nextday = []
        fishspawned = 0
        for fish in data:
            if fish == 0:
                nextday.append(6)
                fishspawned += 1
            else:
                nextday.append(fish-1)
        nextday.extend([8]*fishspawned)
        data = [*nextday]
        # print(len(data), "--", data)
        print(day)
    print(len(data))


@timeit
def star2(data, days):
    distribution = defaultdict(int)
    for _ in data:
        distribution[_] += 1

    for day in range(days):
        newdist = defaultdict(int)
        newdist[0] = distribution[1]
        newdist[1] = distribution[2]
        newdist[2] = distribution[3]
        newdist[3] = distribution[4]
        newdist[4] = distribution[5]
        newdist[5] = distribution[6]
        newdist[6] = distribution[7]
        newdist[7] = distribution[8]
        newdist[8] = distribution[0]
        newdist[6] += distribution[0]

        distribution = newdist
    print(day, sum(distribution.values()))


# def star2_linked_list(data):
#     mydata = LinkedList()
#     for d in data:
#         mydata.append(Node(d))
#     print(str(mydata))
#     # return

#     for day in range(256):
#         tail = mydata.tail
#         fish = mydata.head
#         added = 0
#         count = mydata.length
#         c = 0
#         # while fish != tail.next:
#         while c < count:
#             if fish.value == 0:
#                 mydata.append(Node(8))
#                 fish.value = 6
#                 added += 1
#             else:
#                 fish.value -= 1
#             fish = fish.next
#             c += 1
#         # print(day, mydata.length, "--", str(mydata))
#         print(day, added, mydata.length)
#     print(mydata.length)

star2(data, 80)
star2(data, 256)