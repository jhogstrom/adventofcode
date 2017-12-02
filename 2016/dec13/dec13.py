def iswall(x, y):
    magicnum = 1364
    #magicnum = 10
    r = bin(((x * x) + (3 * x) + (2 * x * y) + y + (y * y)) + magicnum)
    #print(r, r[2:])
    cnt = 0
    for c in r[2:]:
        if c == '1': cnt += 1
    #print(r)
    return cnt % 2 != 0

def canmove(x, y, dir):
    if x < 0:
        print("Outside x", dir, x, y)
        return False
    if y < 0:
        print("Outside y", dir, x, y)
        return False

    beenbefore = board[y][x] != 0
    if beenbefore: print("Been before", dir, x, y, board[y][x])
    coordiswall = iswall(x, y) #board[y][x][0]
    if coordiswall: print("Is wall", dir, x, y)
    return not beenbefore and not coordiswall

targetx = 31
targety = 39
#targetx = 7
#targety = 11

def findpath(x, y, path, dir):
    #print("At", x, y, "steps:", len(path), path)

    if (x == targetx) and (y == targety):
        print("Done. On ", x, y, "length", len(path))
        return True

    if not canmove(x, y, "here"): return False
    board[y][x] = 1
    print(dir, "Visiting: ", x, y, "Steps:", len(path))

    path.append([(x, y)])
    if findpath(x+1, y, path, "east") or \
        findpath(x, y+1, path, "south") or \
        findpath(x-1, y, path, "west") or \
        findpath(x, y-1, path, "north"): return True

    print ("XX STUCK!!", x, y)
    return False

#print(iswall(1, 1))
#exit()
board = []
for y in range(1000):
    r = []
    for x in range(1000):
        r.append(0)
    board.append(r)

path = []
findpath(1, 1, path, "here")
print(len(path))


#print(board)

