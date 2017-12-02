lines = [ l.strip() for l in open('dec03.txt', 'r').readlines()]

valid = 0
c = 0
for l in lines:
    #print(l.split())
    t = sorted([int(s) for s in l.split()])
    if t[0] + t[1] > t[2]: valid += 1
    c += 1

print(c, valid)

valid = 0
c = 0

def gettriangle(l1, l2, l3, col):
    return sorted(
        [
            int(l1.split()[col]),
            int(l2.split()[col]),
            int(l3.split()[col])
        ]
    )


for i in range(0, len(lines), 3):
    print(lines[i])
    print(lines[i+1])
    print(lines[i+2])
    for col in range(3):
        t = gettriangle(lines[i], lines[i+1], lines[i+2], col)
        print(t)
        if t[0] + t[1] > t[2]: valid += 1
        c += 1
print(c, valid)