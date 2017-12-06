b,s,c=[4,1,15,12,0,9,9,5,5,8,7,3,14,5,12,3],[],0
while 1:
 x=str(b)
 if x in s:print(c-s.index(x));break
 s.append(x);c+=1;p=b.index(max(b));v=b[p];b[p]=0
 for i in range(p+1,p+v+1):b[i%16]+=1
print(c)

exit()

b = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]
#banks = [0, 2, 7, 0]
seen, c = [], 0
print(b)
while 1:
    if str(b) in seen:
        print(c - seen.index(str(b)))
        break
    seen.append(str(b))
    c += 1

    p = b.index(max(b))
    v = b[p]
    b[p] = 0
    for i in range(p+1, p + v+1):
        b[i % len(b)] += 1
        #print(i, i % len(b), banks[i % len(b)])
    #print(b)

print(c)

#2392
#6681