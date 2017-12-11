inp = list(map(int,open('10.txt').read().split(",")))
data = list(range(256))

#inp = [3, 4, 1, 5]
#data = [0, 1, 2, 3, 4]

datalen = len(data)
skip = 0
pos = 0

for i in inp:
    # Find selection
    endpos = (pos + i)
#    selection = []
#    for d in range(pos, endpos):
#        selection.append(data[d % datalen])
    selection = [data[d % datalen] for d in range(pos, endpos)][::-1]
    # reverse selection
#    selection = selection[::-1]

    i = 0
    for d in range(pos, endpos):
        data[d % datalen] = selection[i]
        i += 1
    # move pointer
    pos = (pos + i + skip) % datalen
    #increase skip size
    skip +=1

print(inp)
print(data)
print(data[0] * data[1])