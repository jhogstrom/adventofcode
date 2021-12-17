import os
from timer import timeit
from collections import defaultdict, deque

stardate = 17
dataname = f"dec{stardate}.txt"
dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")

def deltax(x_vel):
    if x_vel == 0:
        return 0
    if x_vel > 0:
        return -1
    return 1

@timeit
def star1(targetarea: str):
    _, coords = targetarea.split(":")
    target = coords.strip().split(", ")
    target[0] = target[0].split("..")
    target[0][0] = target[0][0].replace("x=", "")
    target[1] = target[1].split("..")
    target[1][0] = target[1][0].replace("y=", "")
    for i in range(2):
        for j in range(2):
            target[i][j] = int(target[i][j])

    p = [0, 0]
    velocity = [76, 76]
    x, y = 0, 1
    best_y = 0
    found = 0
    for xvel in range(0, 152):
        for yvel in range(-160, 400):
            p = [0, 0]
            velocity = [xvel, yvel]
            c = 0
            max_y = 0
            while True:
                p[x] += velocity[x]
                p[y] += velocity[y]
                velocity[0] += deltax(velocity[0])
                velocity[y] -= 1
                max_y = max([max_y, p[y]])
                # print(f"{p} v={velocity} MAX {max_y} Target: {target}")
                if target[x][0] <= p[x] <= target[x][1] \
                    and target[y][0] <= p[y] <= target[y][1]:
                    print(f"FOUND {max_y} @ {(xvel, yvel)}")
                    best_y = max([max_y, best_y])
                    found += 1
                    break
                c += 1
                if p[x] > max(target[x]) or p[y] < min(target[y]):
                    # print(c, "overshoot")
                    break

    print("Highest", best_y)
    print("Found", found)


@timeit
def star2(data):
    ...

data2 = data[:]
star1(data[0])
star2(data2)