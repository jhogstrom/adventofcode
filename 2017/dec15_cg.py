print(2**31-1)
print(2147483647)
#exit()
A,B=277,349
r=i=0
def n(G,m,d):
 while 1:
  G=G*m%2147483647
  if G%d==0:return G
while i<5e+6:
 A=n(A,16807,4);B=n(B,48271,8);i+=1
 if A&65535==B&65535:r+=1
exit(r)
exit()

A,B,d=277,349,2147483647;r=i=0
while i<4e+7:
 A=A*16807%d;B=B*48271%d;i+=1
 if A&65535==B&65535:r+=1
exit(r)