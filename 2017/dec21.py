inp = [l.split() for l in open('dec21.txt')]
#inp = [l.split() for l in open('dec21ex.txt')]
#print(inp)
match = []
for l in inp:
    inputpattern = l[0].split("/")
    outputpattern = l[2].split("/")
    match.append([inputpattern, outputpattern])

#print (match)

#print("123"[-1])

def makenumber(s):
    i = res = 0
    while len(s) > 0:
        if s[-1] == "#": res += 2**i
        i += 1; s = s[:-1]
    return res

#print(makenumber("#..."))


def rotate(m):
    #print("rotating", m)
    res = set()
    if len(m)==4:
        for i in range(4):
            res.add(makenumber(m))
            m = m[2] + m[0] + m[3] + m[1]
            #print(i, len(m), m)
    if len(m) == 9:
        for i in range(4):
            res.add(makenumber(m))
            m = m[6] + m[3] + m[0] + m[7] + m[4] + m[1] + m[8] + m[5] + m[2]
            #print(i, len(m), m)
        #print("first   ", m)
        m = m[2] + m[1] + m[0] + m[5] + m[4] + m[3] + m[8] + m[7] + m[6]
        #print("reversed", m)
        for i in range(4):
            res.add(makenumber(m))
            m = m[6] + m[3] + m[0] + m[7] + m[4] + m[1] + m[8] + m[5] + m[2]
            #print(i, len(m), m)
        #print(sorted(res))
    return res

def makestr(m):
    res = ""
    if len(m) == 2:
        return m[0] + m[1]
    elif len(m) == 3:
        return m[0] + m[1] + m[2]

def rotations(m):
    res = rotate(makestr(m))
    return res

#print(match)
rs = []
rules2 = dict()
rules3 = dict()

for r in match:
    if len(r[0]) == 3:
        for x in rotations(r[0]):
            rs.append(x)
            rules3[x] = r[1]
    if len(r[0]) == 2:
        for x in rotations(r[0]):
            rs.append(x)
            rules2[x] = r[1]

#print(rules2)
#print(rules3)

def printmatrix(matrix):
    c = 0
    print("MATRIX")
    for m in matrix:
#        print(m)
        for i in m:
            if i == "#": c+=1
    print("--- Count: {} ---".format(c))

matrix = [".#.", "..#", "###"]


def makematrix(chunks, newblock):
    #print("new", len(newblock))
    res = []
    #print("chunks", chunks)
    for y in range(chunks):
        for l in range(len(newblock[0])):
            s = ""
            for x in range(chunks):
                #print("Want: {} Have {} (x/y: {}/{}  {})"\
                #      .format(y*chunks + x, len(newblock), x, y, chunks))
                b = newblock[y*chunks + x]
                s += b[l]
#                print("b", b)
            res.append(s)
    return res

printmatrix(matrix)
for i in range(18):
    if len(matrix) % 2 == 0:
        print(i, "-- 2 => 3  Size: {} Chunks: {}".format(len(matrix), len(matrix) // 2))

        chunks = len(matrix) // 2
        newblock = []
        oldblock = []
        for y in range(chunks):
            for x in range(chunks):
                block = [matrix[y * 2 + 0][x * 2:(x + 1) * 2],
                         matrix[y * 2 + 1][x * 2:(x + 1) * 2]]
                oldblock.append(block)
#                print("b2: ", block)
                n = makenumber(makestr(block))
                r = rules2[n]
                newblock.append(r)
        matrix = makematrix(chunks, newblock)
        print("Old blocks", oldblock)
        print("New blocks", newblock)
    elif len(matrix) % 3 == 0:
        print(i, "-- 3 => 4  Size: {} Chunks: {}".format(len(matrix), len(matrix) // 3))
        chunks = len(matrix) // 3
        newblock = []
        for y in range(chunks):
            for c in range(chunks):
                block = [matrix[y * 3 + 0][c * 3:(c + 1) * 3],
                         matrix[y * 3 + 1][c * 3:(c + 1) * 3],
                         matrix[y * 3 + 2][c * 3:(c + 1) * 3]]
                #print("b: ", block)
                n = makenumber(makestr(block))
                r = rules3[n]
                newblock.append(r)
        matrix = makematrix(chunks, newblock)
    printmatrix(matrix)

printmatrix(matrix)