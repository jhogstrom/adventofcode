def star1():
    r = [i**2 for i in range(1, 100)[::2]]

    print(r)

    for i in range(1, 1000)[::2]:
        if i**2 > 312051:
            print(i, (i)**2)
            break
    print(i)
    print((i-1)/2)
    print(i**2 - 312051)
    #312051

grid = { (0, 0): 1}

def neighborvalue(x, y):
    res = 0
    if (x, y) in grid:
        res = grid[x, y]
    #print("({}, {}) - {}".format(x, y, res))
    return res

def setgrid(d, x, y, v):
    s = neighborvalue(x + 1, y + 1) + \
        neighborvalue(x + 1, y + 0) + \
        neighborvalue(x + 1, y - 1) + \
        \
        neighborvalue(x + 0, y + 1) + \
        neighborvalue(x - 1, y + 1) + \
        \
        neighborvalue(x - 1, y + 0) + \
        \
        neighborvalue(x - 1, y - 1) + \
        neighborvalue(x + 0, y - 1)

    grid[(x, y)] = s
    #print("{} - [{}] ({}, {}) Value: {}".format(v, d, x, y, s))
    print(v, s)
    if s > 312051:

        exit()

def star2():

    #print(grid)

    prevc = 1
    px = 0
    py = 0
    highc = 1
    for r in range(1, 300):
        c = ((r*2)+1)**2
        diff = c - prevc
        qdiff = diff // 4
        #print(r, c, qdiff)
        px += 1
        for p in range(qdiff):
            highc += 1
            setgrid("up", px, py, highc)
            if p != qdiff-1:
                py += 1

        for p in range(qdiff):
            highc += 1
            px -= 1
            setgrid("left", px, py, highc)
        for p in range(qdiff):
            highc += 1
            py -= 1
            setgrid("down", px, py, highc)
        for p in range(qdiff):
            highc += 1
            px += 1
            setgrid("right", px, py, highc)
        prevc = c

    #print(grid)


star2()