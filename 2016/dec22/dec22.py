lines = [ l.strip() for l in open('dec22.txt', 'r').readlines()]

_size = 1
_used = 2
_avail = 3
disks = []
avail = []
used = []
for l in lines:
    if l.startswith("/"):
        parts = l.split(" ")
        data = []
        for p in parts:
            if p.strip() != "":
                data.append(p)
        data[_size] = int(data[_size].replace("T", ""))
        data[_used] = int(data[_used].replace("T", ""))
        data[_avail] = int(data[_avail].replace("T", ""))
        disks.append(data)
        avail.append(data[_avail])
        used.append(data[_used])

used.sort()
avail.sort()


print(disks)
viable = 0
for A in range(len(disks)):
#    if disks[A][_used] == 0:
#        print("==> ZERO", A, disks[A])
#        continue
    for B in range(len(disks)):
        if A != B and disks[A][_used] <= disks[B][_avail] and disks[A][_used] > 0:
            viable += 1
            print(viable, A, B, disks[A], disks[B])
#    print(A)
print(len(disks))
print(viable)
print(used[:5])
print(used[:-60:-1])
print(avail[:-6:-1])