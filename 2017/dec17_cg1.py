b,p=[0],0
for i in range(1,2018):p=1+(p+348)%i;b.insert(p,i);
exit(b[b.index(i)+1])
