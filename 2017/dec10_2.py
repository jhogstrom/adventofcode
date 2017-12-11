rawinp = open('10.txt').read()
data = list(range(256))

#rawinp = "3,4,1,5"
#data = [0, 1, 2, 3, 4]
#rawinp="1,2,3"
#rawinp = ""
#rawinp = "AoC 2017"
inp = [ord(c) for c in rawinp] + [17, 31, 73, 47, 23]

#print(inp)
#exit()

datalen = len(data)
skip = 0
pos = 0

for r in range(64):
    for i in inp:
        # Find selection and reverse it
        endpos = (pos + i)
        selection = [data[d % datalen] for d in range(pos, endpos)][::-1]

        i = 0
        for d in range(pos, endpos):
            data[d % datalen] = selection[i]
            i += 1
        # move pointer
        pos = (pos + i + skip) % datalen
        #increase skip size
        skip +=1

res = ""
for i in range(16):
    d = data[i*16:i*16 + 16]
    r = 0
    for c in d:
        r ^= c

    res += hex(r).split('x')[-1]
print(inp)
print(data)
print(res)