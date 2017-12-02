lines = [ l.strip() for l in open('dec02.txt', 'r').readlines()]

xpos = 2
ypos = 4


def harmonize(p, step):
    p += step
    if p == 0: return 1
    if p == 4: return 3
    return p


def getdigit(xpos, ypos):
    if xpos == 1 and ypos == 1: return 1
    if xpos == 2 and ypos == 1: return 2
    if xpos == 3 and ypos == 1: return 3

    if xpos == 1 and ypos == 2: return 4
    if xpos == 2 and ypos == 2: return 5
    if xpos == 3 and ypos == 2: return 6

    if xpos == 1 and ypos == 3: return 7
    if xpos == 2 and ypos == 3: return 8
    if xpos == 3 and ypos == 3: return 9

keyboard = [
    "......."
    "...1...",
    "..234..",
    ".56789.",
    "..abc..",
    "...d...",
    "......."]


def harmonize2(x, y, axis, step):
    if axis == "x":
        res = x + step
        if getdigit2(res, y) == ".":
            return x
        return res

    res = y + step
    if getdigit2(x, res) == ".":
        return y
    return res


def getdigit2(xpos, ypos):
    return keyboard[ypos][xpos]


for l in lines:
    for c in l:
        if c == "R": xpos = harmonize2(xpos, ypos, "x", 1)
        if c == "L": xpos = harmonize2(xpos, ypos, "x", -1)
        if c == "U": ypos = harmonize2(xpos, ypos, "y", -1)
        if c == "D": ypos = harmonize2(xpos, ypos, "y", 1)
    print(getdigit2(xpos, ypos))
