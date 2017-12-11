i, a = map(int, open('10.txt').read().split(",")), list(range(256))
l=256;k=p=0
for c in i:
    e,c = (p + c),0;s = [a[d % l] for d in range(p, e)][::-1]
    for d in range(p, e):a[d % l] = s[c];c += 1
    p = (p + c + k) % l;k +=1
print(a[0] * a[1])