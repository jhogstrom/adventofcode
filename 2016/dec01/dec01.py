def getdir(d):
    if d == NORTH: return "N"
    if d == EAST: return "E"
    if d == SOUTH: return "S"
    if d == WEST: return "W"
    return "XXXXXX"

l = open('input.txt', 'r').read()
moves = [m.strip() for m in l.split(",")]

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
upmoves = 0
sidemoves = 0
direction = NORTH
coords = [(0, 0)]


def addcoord(c, coords, d):
    print(getdir(d), c)
    try:
        if coords.index(c) > -1:
            print("===")
            print(c, abs(c[0] + abs(c[1])))
            exit()
    except ValueError:
        coords.append(c)



for m in moves:
    print(m)
    d = m[0]
    steps = int(m[1:])

    if d == "L":
        direction -= 1
    else:
        direction += 1

    if direction == -1:
        direction = WEST
    if direction == 4:
        direction = NORTH


    if direction == NORTH:
        for p in range(upmoves+1, upmoves+steps+1):
            addcoord((sidemoves, p), coords, direction)

    if direction == SOUTH:
        for p in range(upmoves-1, upmoves-steps-1, -1):
            addcoord((sidemoves, p), coords, direction)

    if direction == EAST:
        for p in range(sidemoves+1, sidemoves+steps+1, 1):
            addcoord((p, upmoves), coords, direction)

    if direction == WEST:
        for p in range(sidemoves-1, sidemoves-steps-1, -1):
            addcoord((p, upmoves), coords, direction)


    if direction == NORTH:
        upmoves += steps
    if direction == SOUTH:
        upmoves -= steps;
    if direction == EAST:
        sidemoves += steps
    if direction == WEST:
        sidemoves -= steps
    c = (sidemoves, upmoves)

#    try:
#        if coords.index(c) > -1:
#            print(abs(upmoves) + abs(sidemoves))
#            break
#    except ValueError:
#        coords.append(c)
#    print (d, steps, getdir(direction), upmoves, sidemoves)

print(abs(upmoves) + abs(sidemoves))