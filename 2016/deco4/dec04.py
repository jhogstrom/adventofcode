lines = [ l.strip() for l in open('dec04.txt', 'r').readlines()]
alphabet = "abcdefghijklmnopqrstuvwxyz"

sectoridsum = 0
for l in lines:
    parts, checksum = [ s.replace("-", "").replace("]", "") for s in l.split("[")]
    name = sectorid = ""

    for c in parts:
        if c.isalpha(): name += c
        else: sectorid += c
    #name = sorted(name)


    frequency = { c : 0 for c in alphabet}
    #frequency = {"a": 0}
    #print(thischecksum, name)
    for c in name:
        frequency[c] += 1

    res = []
    for c in alphabet:
        res.append(str(9-frequency[c]) + c)
    res = sorted(res)

    thischecksum = ""
    for i in range(5):
        thischecksum += res[i][1]
    if thischecksum == checksum:
        #print(checksum, thischecksum, res)
        sectoridsum += int(sectorid)

        name = l.split("[")[0]
        #print(name)
        decrypted = ""
        for c in name:
            if c.isdigit(): continue
            if c == "-":
                decrypted += " "
                continue
            p = alphabet.index(c)
            p += int(sectorid)
            p = p % len(alphabet)
            decrypted += alphabet[p]
        print(decrypted, sectorid)
print(sectoridsum)