m = 0
while 1:
    c, a = 0, dict()
    for l in open('13ex.txt'): l, d = map(int, l.split(":"));a[l] = 2 * d - 2
    for i in a:
        if (i + m) % a[i] == 0: c += 1;break
    if m % 10000 == 0: print(m)
    if not c: exit(m)
    m += 1
print(m)

exit()

def init():
    a = dict()
    for l in open('13ex.txt').readlines():
        l, d = map(int, l.split(":"))
        a[l] = 2 * d - 2
    return a

m=0

while 1:
    c=0
#    a = dict()
    for l in open('13ex.txt'):l, d = map(int, l.split(":"));a[l] = 2 * d - 2
    for i in a:
        if(i+m)%a[i] == 0:c += 1
    if not c: break
    m += 1

print(c, m)

print("round should be larger than 171428")