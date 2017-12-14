z=range
def ip(n):
    return {0:"",1:"1",2:"10",3:"11",4:"100",5:"101",6:"110",7:"111",8:"1000",9:"1001",10:"1010",11:"1011",12:"1100",13:"1101",14:"1110",15:"1111"}[n].zfill(4)

def h(s):
    t=list(z(256));l=256;k=p=0;res=""
    inp=[ord(c) for c in s]+[17,31,73,47,23]
    for q in z(64):
        for i in inp:
            e,i=p+i,0;s=[t[d%l] for d in z(p,e)][::-1]
            for d in z(p, e):t[d%l]=s[i];i+=1
            p=(p+i+k)%l
            k+=1
    for i in z(16):
        v,r=t[i*16:i*16+16],0
        for n in v:r^=n
        res+=ip(r//16)+ip(r%16)
    return res

k = "jxqlasbh";u=g=0;x=[]
for c in z(128):x.append([x!="1" for x in h(k+"-"+str(c))])

def ms(row, col):
    r=row;c=col
    if x[r][c]:return
    x[r][c]=True
    if c+1<=127 and not x[r][c+1]:ms(r,c+1)
    if c-1>=0 and not x[r][c-1]:ms(r,c-1)
    if r+1<=127 and not x[r+1][c]:ms(r+1,c)
    if r-1>=0 and not x[r-1][c]:ms(r-1,c)

for i in z(128):
    for j in z(128):
        if not x[i][j]:ms(i,j);g+=1

print(g)
