a=list("abcdefghijklmnop")
for m in open('1').read().split(","):
 o=m[1];p=m[1:].split("/")
 if o=="s":t=-int(p);a=a[t:]+a[0:t]
 elif o=="x":x,y=map(int,p);o=1
 elif o=="p":x,y=[a.index(c) for c in p];o=1
 if o==1:a[x],a[y]=a[y],a[x]
print(a)

print("padheomkgjfnblic")
