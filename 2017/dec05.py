code = [int(l.strip()) for l in open('5.txt', 'r').readlines()]
#code = [0, 3, 0, 1, -3]

p, c = 0, 0
print(c, p, code[p], code)
while True:
    j = -1 if code[p] >= 3 else 1
    #j = 1
    code[p] += j
    p += code[p] - j
    c += 1
    #print(c, p, code[p] if p < len(code) else "done", code)
    if (p >= len(code)):
        break

print("Correct", 28178177)
print(c)