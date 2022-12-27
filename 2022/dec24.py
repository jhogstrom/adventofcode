from collections import defaultdict
import os

runtest = False
stardate = 24
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


def parse(data):
    res = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            res[(x-1, y-1)] = [c] if c in "<>v^#" else []
    return res


def print_slice(m, mx, my, start=None, goal=None, curr=None):
    for y in range(-1, my+1):
        s = []
        for x in range(-1, mx+1):
            a = m[(x, y)]
            if (x, y) == curr:
                s.append("X")
            elif (x, y) in [start, goal]:
                s.append("_")
            else:
                s.append(" " if len(a) == 0 else a[0] if len(a) == 1 else str(len(a)))
        print(f'{y:>3} {"".join(s)}')
    print("----")


def evolve(m, mx, my):
    moves = {
        '<': -1,
        '>': 1,
        'v': 1,
        '^': -1
    }
    res = [m]
    for t in range(mx*my-1):
        time_slice = defaultdict(list)
        for cell, content in res[-1].items():
            for w in content:
                nx, ny = cell
                if w in "<>":
                    nx += moves[w]
                    nx %= mx
                elif w in "v^":
                    ny += moves[w]
                    ny %= my
                time_slice[(nx, ny)].extend(w)
        res.append(time_slice)
    print("Time evolved")
    return res


def neighbors(n, mx, my):
    x, y = n
    res = [
                 (x, y-1),
        (x-1, y), (x, y), (x+1, y),
                 (x, y+1)
        ]
    return [_ for _ in res if -1 <= _[0] <= mx and -1 <= _[1] <= my]


def solve(m, mx, my, start, goal, start_time=0) -> int:
    print(f">> Going from {start} to {goal} starting @ {start_time}.")
    open_nodes, seen = [(start, start_time)], set()
    steps = 0
    while open_nodes:
        steps += 1
        curr, ix = open_nodes[0], 0
        for i, _ in enumerate(open_nodes):
            if _[1] < curr[1]:
                ix = i
        curr = open_nodes.pop(ix)
        t = curr[1]
        # if steps % 1000 == 0:
        #     print(steps, t, curr)
        if (curr[0], t % (mx*my)) in seen:
            continue
        seen.add((curr[0], t % (mx*my)))
        t += 1
        for n in neighbors(curr[0], mx, my):
            if (n, t % (mx*my)) in seen:
                continue
            # Need to check if target is empty -
            # this excludes edges and blizzards
            if len(m[t % (mx*my)][n]) == 0:
                open_nodes.append((n, t))
            if n == goal:
                print(f"<< Arrived at {goal} after {t-start_time} minutes")
                return t - start_time

    raise ValueError(f"{goal} not found after {curr[1]+1} steps.")


def star1(data) -> int:
    m = parse(data)
    my = len(data) - 2
    mx = len(data[0]) - 2
    temporal_map = evolve(m, mx, my)
    return solve(temporal_map, mx, my, (0, -1), (mx-1, my))


def star2(data) -> int:
    m = parse(data)
    my = len(data) - 2
    mx = len(data[0]) - 2
    temporal_map = evolve(m, mx, my)

    j1 = solve(temporal_map, mx, my, (0, -1), (mx-1, my), 0)
    j2 = solve(temporal_map, mx, my, (mx-1, my), (0, -1), j1)
    j3 = solve(temporal_map, mx, my, (0, -1), (mx-1, my), j2+j1)
    return j1 + j2 + j3


print("star1:", star1(data))
print("star2:", star2(data))
