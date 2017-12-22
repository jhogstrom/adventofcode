from collections import defaultdict as d
p=[l for l in open('2')]
m=d(int)
W=len(p)
def s(x,y):return str(x)+"."+str(y)
for y in range(W):
 for x in range(W):m[s(x,y)]=[0,2][p[y][x]=="#"]
x=y=W//2
r=[[0,-1],[1,0],[0,1],[-1,0]]
d=I=i=0
u={0:3,1:0,2:1,3:2}
t={0:1,1:2,2:3,3:0}
while i<1e+7:i+=1;c=s(x,y);d=(d+u[m[c]])%4;m[c]=t[m[c]];I+=[0,0,1,0][m[c]];x+=r[d][0];y+=r[d][1]
print(I)