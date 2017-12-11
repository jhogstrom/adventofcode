r=range
d, l, I = list(r(256)), 256, [ord(c) for c in open('10.txt').read()] + [17, 31, 73, 47, 23]
K=p=0
for k in r(64):
    for i in I:
        e, j= (p + i), 0;s= [d[c % l] for c in r(p, e)][::-1]
        for c in r(p, e):d[c % l]=s[j];j+=1
        p= (p + i + K) % l;K+=1

R = ""
for i in r(16):
    k=0
    for c in d[i*16:i*16+16]:k^=c
    R+=hex(k)[2:]

print(R)
print("decdf7d377879877173b7f2fb131cf1b")
