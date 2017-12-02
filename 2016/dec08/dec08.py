lines = [ l.strip() for l in open('dec08.txt', 'r').readlines()]

board = [[" " for i in range(50)] for i in range(6)]


def turnon(x, y):
    print(x, y)
    for r in range(y):
        for c in range(x):
            board[r][c] = "X"

def printboard():
    count = 0
    for row in board:
        r = ""
        for c in row:
            r += c
            if c == "X":
                count += 1
        print(r)
        #print (count)


def rotatecolumn(col, offset):
    s = ""
    for i in board:
        s += i[col]

    res = [" " for i in range(8)]
    for i in range(len(s)):
        res[(i+offset)%len(s)] = s[i]

    for i in range(len(board)):
        board[i][col] = res[i]


def rotaterow(row, offset):
    s = ""
    for c in board[row]:
        s += c

    res = [" " for i in range(50)]
    for i in range(len(s)):
        res[(i + offset) % len(s)] = s[i]

    for i in range(50):
        board[row][i] = res[i]


for l in lines:
    print(l)
    if l.startswith("rect"): #rect 6x1
        p = l.split(" ")
        x, y = p[1].split("x")

        turnon(int(x), int(y))
        printboard()
        continue
    if l.startswith("rotate column"): #rotate column x=23 by 3
        p = l.split(" ")
        col = int(p[2].split("=")[1])
        offset = int(p[4])
        rotatecolumn(col, offset)
        continue
    if l.startswith("rotate row"): #rotate row y=4 by 8
        p = l.split(" ")
        row = int(p[2].split("=")[1])
        offset = int(p[4])
        rotaterow(row, offset)

printboard()