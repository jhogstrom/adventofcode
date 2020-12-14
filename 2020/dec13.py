import os
import itertools
from timing import timeit
import enum

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]

# data = [
# "939",
# "7,13,x,x,59,x,31,19"]

departure = int(data[0])
busses = data[1].split(",")

@timeit
def star1():
    global busses

    busses_1 = [int(_) for _ in busses if _ != "x"]

    deps = {departure // _ * _ + _ : _ for _ in busses_1}
    # print(f"best arrival times: {deps}")

    m = min(deps)
    # print(f"min: {m}")
    # print(f"wait: {m-departure}")
    return (m-departure)*deps[m]
    print(f"* {(m-departure)*deps[m]}")

def star2_core(data_arr, start_t=0):
    # Parse input
    delay = 0
    deps = {}
    offset = {}
    for _ in data_arr:
        if isinstance(_, int):
            deps[_] = delay
            offset[_] = 0
        delay += 1

    offset[data_arr[0]] = start_t

    # Get the biggest number to use for stepping t
    increment = max(deps)

    # Find offset for biggest number
    delay_offset = deps[increment]

    # Adjust offsets
    deps = {k: v-delay_offset for k, v in deps.items()}

    # Start searching
    t = start_t
    found = False

    while True:
        if all([(t+deps[_]-offset[_]) % _ == 0 for _ in deps]):
            # This is the first minute meeting the criteria.
            if not found:
                first_t = t
                # However, we also need to find the cycletime, which is indicated by the second hit.
                found = True
            else:
                # we return the first time (first-t minus the delay_offset we used) and the cycle time.
                return first_t-delay_offset, t-first_t
        t += increment


@timeit
def star2():
    global busses
    d = []
    c = 0
    start_t = 0
    numcount = 0

    # Split into items
    for s in busses:
        # Convert numbers to ints - and memorize we added one number
        if s.isnumeric():
            d.append(int(s))
            numcount += 1
        else:
            d.append(s)

        # When we have two numbers, check the time and cycle time
        if numcount == 2:
            t, cycle = star2_core(d, start_t)
            start_t = t - cycle
            # Reset the array with the cycletime (new virtual bus line) and add appropriate amount of x
            d = [cycle] + ["x"] * c
            numcount = 1
        c += 1
    return t


print(f"* {star1()}")
r = star2()
print(f"** {r}")
