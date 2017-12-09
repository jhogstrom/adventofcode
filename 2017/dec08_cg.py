m,h=dict(),0
def x(r,o,v):
    if not r in m:m[r]=0
    if o:m[r]+=v
    else:m[r]-=v
for l in [l.strip() for l in open('8.txt')]:
    p=l.split();r=p[0]
    if eval(str(m.get(p[4],0))+p[5]+p[6]):x(r,p[1]=="inc",int(p[2]))
    h = max([m[r],h])
print(max(m.values()),h)
print("Expected: 8022 9819")