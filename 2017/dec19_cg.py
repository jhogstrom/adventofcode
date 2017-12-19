print("BPDKCZWHGT 17728")
I=[l for l in open('19.txt')]
d=D=[0,1];U,L,R=[0,-1],[-1,0],[1,0]
y=i=0;x=I[0].index('|');p=c=""
def C(x,y,d):x+=d[0];y+=d[1];return y^x and y<len(I)and x<len(I[y])and I[y][x]in"|-"
while c!=" ":
 i+=1;x+=d[0];y+=d[1];c=I[y][x]
 if c.isalpha():p+=c
 if c=="+":
  if d in[D,U]:d=L if C(x,y,L)else R
  else:d=U if C(x,y,U)else D
print(p,i)
