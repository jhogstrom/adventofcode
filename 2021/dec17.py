import os
from timer import timeit
from collections import defaultdict, deque

stardate = 17
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
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
    x, y = 0, 1
    _, coords = targetarea.split(":")
    target = coords.strip().split(", ")
    target[0] = target[0].split("..")
    target[0][0] = target[0][0].replace("x=", "")
    target[1] = target[1].split("..")
    target[1][0] = target[1][0].replace("y=", "")
    for i in range(2):
        for j in range(2):
            target[i][j] = int(target[i][j])

    targets = [
        set(range(min(target[x]), max(target[x])+1)),
        set(range(min(target[y]), max(target[y])+1))]

    best_y = 0
    found = 0
    # Somewhat arbitrary ranges in x and y
    for xvel in range(14, 152):
        for yvel in range(-156, 156):
            max_y = 0
            p = [0, 0]
            velocity = [xvel, yvel]
            while True:
                p[x] += velocity[x]
                p[y] += velocity[y]
                velocity[x] += deltax(velocity[x])
                velocity[y] -= 1
                max_y = max([max_y, p[y]])
                # print(f"{p} v={velocity} MAX {max_y} Target: {target}")
                if p[x] in targets[x] and p[y] in targets[y]:
                    # print(f"FOUND {max_y} @ {(xvel, yvel)}")
                    best_y = max([best_y, max_y])
                    found += 1
                    break
                # Not necessarily handling target in all quadrants...
                if p[x] > max(target[x]) or p[y] < min(target[y]):
                    # print(c, "overshoot")
                    break

    print("Star1: Highest", best_y)
    print("Star2: Found", found)


star1(data[0])
