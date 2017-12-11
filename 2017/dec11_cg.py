from collections import defaultdict
x,s=defaultdict(int),0
def dist():
    e=abs(x["ne"]+x["se"]-x["nw"]-x["sw"])
    return e+x["n"]-x["s"]+(x["ne"]-x["sw"]+x["nw"]-x["se"]-e)/2
for m in open('11.txt').read().split(","):
    x[m]+=1;s=max(s, dist())
print(s)
print(1426)