lines = [ l.strip() for l in open('dec20.txt', 'r').readlines()]

ranges = []

for l in lines:
    p = [int(x) for x in l.split("-")]
    ranges.append([p[0], p[1]])

ranges.sort()

#for r in ranges:
#    print(r)

print("*" * 80)
mergedranges = [[0, 0]]
for r in ranges:
    if r[0] <= mergedranges[-1][1] + 1:
        mergedranges[-1] = [mergedranges[-1][0], max(r[1], mergedranges[-1][1])]
    else:
        mergedranges.append(r)

print(len(mergedranges))
s = 0
for r in mergedranges:
    print(r)
    s += (1 + r[1] - r[0])

print(4294967295 - s)
#    print(r)
