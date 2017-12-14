# rawinp = "3,4,1,5"
# data = [0, 1, 2, 3, 4]
# rawinp="1,2,3"
# rawinp = ""
rawinp = "flqrgnkx-0"


def mkbin(n):
    binstr={0:"",1:"1",2:"10",3:"11",4:"100",5:"101",6:"110",7:"111",8:"1000",9:"1001",10:"1010",11:"1011",12:"1100",13:"1101",14:"1110",15:"1111"}
    return binstr[n].zfill(4)

def getknothash(s):
    data = list(range(256))
    inp = [ord(c) for c in s] + [17, 31, 73, 47, 23]

    datalen = len(data)
    skip = 0
    pos = 0

    for r in range(64):
        for i in inp:
            # Find selection and reverse it
            endpos = (pos + i)
            selection = [data[d % datalen] for d in range(pos, endpos)][::-1]

            i = 0
            for d in range(pos, endpos):
                data[d % datalen] = selection[i]
                i += 1
            # move pointer
            pos = (pos + i + skip) % datalen
            # increase skip size
            skip += 1

    res = ""
    for i in range(16):
        v = data[i*16:i*16 + 16]
        r = 0
        for n in v:
            r ^= n
        res += mkbin()
        h = hex(r).split('x')[-1].zfill(2)
        res += h
    return res


def knothashtobin(s):
    r = ""
    binstr = {
            '0': "0000",
            '1': "0001",
            '2': "0010",
            '3': "0011",
            '4': "0100",
            '5': "0101",
            '6': "0110",
            '7': "0111",
            '8': "1000",
            '9': "1001",
            'a': "1010",
            'b': "1011",
            'c': "1100",
            'd': "1101",
            'e': "1110",
            'f': "1111"
        }
    for ch in s:
        r += binstr[ch]
#    print(len(s), s)
#    print(len(r), r)
    return r

k = "jxqlasbh"; answer = "1182"
#k = "flqrgnkx"; answer = "1242" # sample key
usage = 0
disk = []
scanned = []
for c in range(128):
    d = "{}-{}".format(k,c)
    b = knothashtobin(getknothash(d))
    for i in b:
        if i == "1": usage += 1
    disk.append(b)
    scanned.append([False for x in range(128)])

for d in disk:
    print(len(d), d)

def markscanned(row, col):
    if disk[row][col] == "0":
        scanned[row][col] = True
    if scanned[row][col]:
        return
#    print("scanning", row, col)
    scanned[row][col] = True
    # go east
    if col + 1 <= 127 and disk[row][col+1] == "1":
        markscanned(row, col+1)
    # go west
    if col - 1 >= 0 and disk[row][col-1] == "1":
        markscanned(row, col-1)
    # go south
    if row + 1 <= 127 and disk[row+1][col] == "1":
        markscanned(row+1, col)
    # go north
    if row-1 >= 0 and disk[row-1][col] == "1":
        markscanned(row-1, col)


# exit()
print("disk generated - starting group search")
groups = 0
for i in range(len(disk)):
    for j in range(len(disk[i])):
        if disk[i][j] == "0":
            scanned[i][j] == True
        if disk[i][j] == "1" and not scanned[i][j]:
            markscanned(i, j)
            groups += 1
            print("groups:", groups)

print("Total (should be {}): {}".format(answer, groups))
