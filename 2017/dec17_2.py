buf = [0]
stride = 348
p = 0

def printbuf(buf, p):
    r = ""
    for j in range(min(100, len(buf))):
        if j == p: r += " ({})".format(buf[j])
        else: r += " {:2}".format(buf[j])
    print("{:3} - {}".format(len(buf), r))

zpos = 0
afterzero = 0
dist = 50000000
target = dist
target = 0
buflen = 1
for i in range(dist):
    if i % 100000 == 0:
        print(i)
    p += stride
    p %= buflen
    p+=1
    if p == zpos + 1:
        afterzero = i+1
#    buf.insert(p, i+1)
    buflen += 1

#    if i % 10000 == 0: print(i)

#printbuf(buf, p)
#p = buf.index(target)
#print(buf[p-1], buf[p], buf[p+1])
print(afterzero)
