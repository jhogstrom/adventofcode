from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "16"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def active_beams(beams):
    return True


def get_next_pos(beam):
    direction = beam[1]
    if direction == ">":
        return (beam[0][0]+1, beam[0][1])
    elif direction == "<":
        return (beam[0][0]-1, beam[0][1])
    elif direction == "^":
        return (beam[0][0], beam[0][1]-1)
    elif direction == "v":
        return (beam[0][0], beam[0][1]+1)
    else:
        raise ValueError(f"Unknown direction {direction}")


# How turns are made:
# | - pass through if coming from up or down, split up and down if coming from left or right
# - - pass through if coming from left or right, split left and right if coming from up or down
# / - turn right if coming from down, turn down if coming from right,
#     turn left if coming from up, turn up if coming from left
# \ - turn left if coming from down, turn down if coming from left,
#     turn right if coming from up, turn up if coming from right

# The turnmap is keys on the cell + direction, and returns the new directions
turnmap = {
    ".>": ">",
    ".<": "<",
    ".^": "^",
    ".v": "v",
    "|>": "v^",
    "|<": "^v",
    "|^": "^",
    "|v": "v",
    "->": ">",
    "-<": "<",
    "-^": "<>",
    "-v": "<>",
    "/>": "^",
    "/<": "v",
    "/^": ">",
    "/v": "<",
    "\\<": "^",
    "\\>": "v",
    "\\^": "<",
    "\\v": ">"
}


def is_outside(pos, data):
    return pos[0] < 0 or pos[0] >= len(data[0]) or pos[1] < 0 or pos[1] >= len(data)


def print_energized(data, seen):
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in seen:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("===")


def count_energized(data, start, direction):
    seen = set()
    traversed = set()
    beams = [(start, direction)]
    traversed.add(beams[0])
    while len(beams) > 0:
        beam = beams.pop()
        newpos = get_next_pos(beam)
        # This beam has left the field, so it's done
        if is_outside(newpos, data):
            continue
        seen.add(newpos)
        newdirections = turnmap[data[newpos[1]][newpos[0]]+beam[1]]
        for d in newdirections:
            newbeam = (newpos, d)
            # Been there in the same direction - no need to traverse again
            if newbeam in traversed:
                continue
            beams.append(newbeam)
            traversed.add(newbeam)
    # print_energized(data, seen)
    return len(seen)


@timeit
def star1(data):
    logging.debug("running star 1")
    res = count_energized(data, (-1, 0), ">")
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    energized = set()
    for y in range(len(data)):
        energized.add(count_energized(data, (-1, y), ">"))
        energized.add(count_energized(data, (len(data[0]), y), "<"))
    for x in range(len(data[0])):
        energized.add(count_energized(data, (x, -1), "v"))
        energized.add(count_energized(data, (x, len(data)), "^"))

    print(max(energized))


star1(data)
star2(data2)
