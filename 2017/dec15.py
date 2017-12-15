A = [277, 16807, 4]
B = [349, 48271, 8]

#A = [65, 16807, 4]
#B = [8921, 48271, 8]

divideBy = 2147483647

def nextnum(G):
    while 1:
        G[0] = (G[0] * G[1]) % 2147483647
        if G[0] % G[2] == 0:
            return G
#    return G

def compare(G1, G2):
    #print(G1[0] & 65535, G2[0] & 65535)
    return (G1[0] & 65535) == (G2[0] & 65535)

r = 0
print(A, B)
for i in range(5000000):
    if i % 10000 == 0: print(i)
    A = nextnum(A)
    B = nextnum(B)

    if compare(A, B):
        r += 1
#        print("found @", i); break

print("expected: 1, actual", r)

