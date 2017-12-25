inp=[list(map(int, l.strip().split("/"))) for l in open('24.txt')]

maxstrength = 0

def buildbridge(bridge, bits, newbridge):
    global maxdepth
    global maxstrength
    l = len(newbridge)
    if l >= maxdepth:
        maxdepth = l
        s = sum(newbridge)
#        if s > maxstrength:
#            maxstrength = s
        print("{:4} - {:4}".format(l, s))
    #print("{}  -- {}".format(nextstart, bits))
    r = 0
    for i in range(len(bits)):
        n = []
        if bits[i][0] == bridge[-1]:
            n = bits[i]
        elif bits[i][1] == bridge[-1]:
            n = bits[i][::-1]

        if len(n) > 0:
            r = max(r, buildbridge(n, bits[:i] + bits[i+1:], newbridge+n))

    return sum(bridge) + r
maxdepth = 0

r = buildbridge([0,0], inp, [0])

#print(">>", maxdepth, maxstrength)

print(r)

# > 1964