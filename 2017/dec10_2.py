rawinp = open('10.txt').read()
data = list(range(256))

rawinp = "3,4,1,5"
#   data = [0, 1, 2, 3, 4]
rawinp="1,2,3"; answer = "3efbe78a8d82f29979031a4aa0b16a9d"
rawinp="1,2,4"; answer = "63960835bcdc130f0b66d7ff4f6a5a8e"
#rawinp = ""; answer =    "a2582a3a0e66e6e86e3812dcb672a272"
#rawinp = "AoC 2017"; answer = "33efeb34ea91902bb2f59c9920caa6cd"
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

    c = hex(r).split('x')[-1]
    if (len(c) == 1): c = "0" + c
    res += c
    print(c, r)
#print(inp)
#print(data)

print("res:", len(res), res)
print("ans:", len(answer), answer)