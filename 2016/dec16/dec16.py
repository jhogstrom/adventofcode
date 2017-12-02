def genstring(s, targetlen):
    while len(s) < targetlen:

        a = s
        s += "0"
        b = ""
        for c in a[::-1]:
            if c == "1": b += "0"
            else: b += "1"
        s = s + b
        print(len(s))
    return s[:targetlen]


def genhash(s):
    res = ""
    while len(res) % 2 == 0:
        #print(s)
        res = ""
        for i in range(0, len(s), 2):
            #print(s[i:i+2])
            if s[i] == s[i+1]:
                res += "1"
            else:
                res += "0"
        s = res
        print(res)
    return res


#print(genhash("10000011110010000111"))
#exit()
inp, dlen = "11101000110010100", 35651584
#inp, dlen = "10000", 20
#10000011111001100000
#10000011111001100000
data = genstring(inp, dlen)
print(data)
print(genhash(data))
exit()

print(genhash("110010110100"))
print(genhash("11"))
print(genhash("001101"))

exit()
print(genstring("1", 3))
print(genstring("0", 3))
print(genstring("11111", 11))
print(genstring("111100001010", 25))