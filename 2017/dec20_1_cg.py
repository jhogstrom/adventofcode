inp = [l.split() for l in open('20.txt')]
V=[]
A = []
for l in inp:
    part = dict()
    for data in l:
        d = data.replace("=<", " ").replace(",", " ").replace(">", "").split()
        part[d[0]] = list(map(int, d[1:]))
    v = sum(map(abs, part["v"]))
    a = sum(map(abs,part["a"]))
    V.append(v)
    A.append(a)

MINA = dict()
minv = max(V)
vi = 0
for i in range(len(A)):
    if A[i] == min(A):
        MINA[i] = V[i]
        if V[i] < minv:
            vi = i
print(vi)
print(MINA[vi])
print(MINA)

#print(MINA)
#for i in MINA:
#    print(i, V[i])
    #print(particles[i])
