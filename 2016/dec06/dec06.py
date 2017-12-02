
lines = [ "eedadn",
"drvtee",
"eandsr",
"raavrd",
"atevrs",
"tsrnev",
"sdttsa",
"rasrtv",
"nssdts",
"ntnada",
"svetve",
"tesnvt",
"vntsnd",
"vrdear",
"dvrsen",
"enarar" ]

lines = [ l.strip() for l in open('dec06.txt', 'r').readlines()]

freq = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
for i in range(8):
    f = {}
    for c in alphabet:
        f[c] = 0
    freq.append(f)

for line in lines:
    for i in range(len(line)):
        oldf = freq[i][line[i]]
        freq[i][line[i]] = freq[i][line[i]] + 1
        #print(i, line, line[i], oldf, "=>", freq[i][line[i]])
    #break

res = ""
for f in freq:
    min = len(lines)
    for c in alphabet:
        if f[c] != 0 and f[c] < min:
            r = c
            min = f[c]
    res += r

for f in freq:
    print(f)
print(res)
