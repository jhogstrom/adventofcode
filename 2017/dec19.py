inp = [l for l in open('19.txt')]
print(inp)
DOWN = [0, 1]
UP = [0, -1]
LEFT = [-1, 0]
RIGHT = [1, 0]

y = 0
x = inp[0].index('|')

dir = DOWN
path = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def canmove(xc, yc, d):
    nx = xc + d[0]
    ny = yc + d[1]
    if ny < 0: return False
    if ny >= len(inp): return False
    if nx < 0: return False
    if nx >= len(inp[ny]): return False
    c = inp[ny][nx]
    return c in "|-"
i =0
while 1:
    i += 1
    x += dir[0]; y += dir[1]
    c = inp[y][x]
    if c in alphabet:
        path += c
        print(i, c, x, y, dir, path)
    if c == "+": # Turning point
        if dir == DOWN or dir == UP:
            if canmove(x, y, LEFT):
                dir = LEFT
            else:
                if not canmove(x, y, RIGHT):
                    print(i, c, x, y, dir, path)
                    print("Unable to turn left/right")
                dir = RIGHT
        else:
            if canmove(x, y, UP):
                dir = UP
            else:
                if not canmove(x, y, DOWN):
                    print(i, c, x, y, dir, path)
                    print("unable to turn up/down)")
                dir = DOWN
    if inp[y+dir[1]][x+dir[0]] == " ": break
    #s = inp[y]
    #s = s[:x] + "*" + s[x+1:]
    #inp[y] = s
    #for l in inp:
    #    print(l.strip())
    #if i > 100: break
print(path)
print(dir)
#wrong:
#BPDKCZHGT
#BPDKCZHGT
#BPDKCZHGT