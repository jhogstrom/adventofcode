buf = [0]
stride = 348
p = 0

def printbuf(buf, p):
    r = ""
    for j in range(min(100, len(buf))):
        if j == p: r += " ({})".format(buf[j])
        else: r += " {:2}".format(buf[j])
    print("{:3} - {}".format(len(buf), r))

dist = 2017000
target = dist
target = 0
for i in range(dist):
    if i % 10000 == 0:
        printbuf(buf, p)
    p += stride
    p %= len(buf)
    buf.insert(p+1, i+1)
    p += 1
#    if i % 10000 == 0: print(i)

printbuf(buf, p)
p = buf.index(target)
print(buf[p-1], buf[p], buf[p+1])

