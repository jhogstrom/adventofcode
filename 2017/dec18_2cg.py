from collections import defaultdict as D
def v(r,n):
 if n in r:return r[n]
 return int(n)
class C:
 def B(self,v):self.q.append(v)
 def U(self,o,T,P):
  O=o[0][1];A=o[1];B=o[-1];r=self.r
  if O=="n":T.B(v(r,A));self.t+=1
  if O=="e":r[A]=v(r,B)
  if O=="d":r[A]+=v(r,B)
  if O=="u":r[A]*=v(r,B)
  if O=="o":r[A]%=v(r,B)
  if O=="c":
   if len(self.q)>0:r[A]=self.q[0];self.q=self.q[1:];self.R=True
   else:self.R=False;return P
  if O=="g":
   if v(r,A)>0:return P+v(r,B);
  return P+1
 def __init__(self):self.r=D(int);self.R=1;self.q=[];self.t=0
X=C();N=0
Y=C();M=0
Y.r["p"]=1
I=[l.strip().split(" ")for l in open('18.txt')]
while 1:
 N=X.U(I[N],Y,N);M=Y.U(I[M],X,M)
 if not(X.R or Y.R):break
exit(Y.t)