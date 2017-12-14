from collections import defaultdict as x
p,g=dict(),x(list)
for l in open('12.txt').readlines():
    n=l.replace(",","").split();p[n[0]]=n[2:]
def s(r,n):
    for c in n:
        if not c in g[r]:g[r].append(c);s(r,p[c])
def c(n):
    for t in g.values():
        if n in t:return True
    return False
for n in p:
    if not c(n):s(n,p[n])
print(len(g['0']),len(g))
print(175, 213)