lines = [
    "abba[mnop]qrst[abba]",
    "abcd[bddb]xyyx",
    "aaaa[qwer]tyui",
    "ioxxoj[asdfgh]zxcvbn"
]

lines = [
    "aba[bab]xyz",
    "xyx[xyx]xyx",
    "aaa[kek]eke",
    "zazbz[bzb]cdb"
]

#lines = [ l.strip() for l in open('dec07.txt', 'r').readlines()]

lines = [ l.replace("[", "-").replace("]", "-") for l in lines]


def containspattern(s):
    res = False
    for i in range(0, len(s) - 3):
        res = res or \
              (s[i] == s[i+3] and \
              s[i+1] == s[i + 2] and \
              s[i] != s[i+1])
        #print(s[i:i+4])
    #if res:
    #    print("v(s):", s)
    return res

#print(containspattern("abba"))
#exit()

count = 0
for l in lines:
    p = l.split("-")
    print(p)
    valid = False
    for s in p[0::2]:
        valid = valid or containspattern(s)
        #print("outside:", s)
    if not valid: continue
    for s in p[1::2]:
        valid = valid and not containspattern(s)
        #print("inside[]:", s)
    if valid:
        count += 1
        print("valid string: ", l)

print(count)


def getABAs(parts):
    res = []
    #print(parts)
    for p in parts:
        #print(p)
        for i in range(0, len(p)-2):
            #print(i, p[i], p[i+2])
            if p[i] == p[i+2] and p[i] != p[i+1]:
                res.append(p[i:i+3])
    #print(res)
    return res

count = 0


def containsBAB(BABs, parts):
    for bab in BABs:
        for p in parts:
            if bab in p:
                print(bab)
                return True

    return False

lines = [
    "aba[bab]xyz",
    "xyx[xyx]xyx",
    "aaa[kek]eke",
    "zazbz[bzb]cdb"
]

lines = [ l.strip() for l in open('dec07.txt', 'r').readlines()]

lines = [ l.replace("[", "-").replace("]", "-") for l in lines]

def reversestrings(strings):
    return [s[1] + s[0] + s[1] for s in strings]

print("====")

for l in lines:
    p = l.split("-")
    #print(p)
    ABAs = getABAs(p[0::2])
    #print(ABAs, reversestrings(ABAs))
    if containsBAB(reversestrings(ABAs), p[1::2]):
        count += 1
        print(count, p)


print(count)