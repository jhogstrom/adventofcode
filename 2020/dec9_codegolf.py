import itertools
o=print
d=[int(_) for _ in open("9").readlines()]
p=d[:25]
for n in d[25:]:
 s=[sum(_) for _ in itertools.combinations(p,2)]
 if n in s:p=p[1:]+[n]
 else:o(n);break
for i in range(len(d)-1):
 for j in range(len(d)):
  s=sum(d[i:j])
  if s>n:break
  if s==n:o(min(d[i:j])+max(d[i:j]));exit()