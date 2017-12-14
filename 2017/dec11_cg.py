from collections import defaultdict as w
x,s=w(int),0
def d():
    e=abs(x["ne"]+x["se"]-x["nw"]-x["sw"])
    return e+x["n"]-x["s"]+(x["ne"]-x["sw"]+x["nw"]-x["se"]-e)/2
for m in open('11.txt').read().split(","):
    x[m]+=1;s=max(s,d())
print(d(),s)
print(1426)