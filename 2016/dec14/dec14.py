import hashlib
from symbol import while_stmt

startcode = "abc"
#startcode = "zpqevtbw"

threedigits = dict()
fivedigits = dict()
count = 0


def genhash(tocheck):
    md5 = tocheck
    for i in range(2017):
        md5 = hashlib.md5(md5.encode('utf-8')).hexdigest()
    return md5


def gethash(k, tocheck, highest):
    keys = fivedigits.keys()
    if len(keys) > 0 and k < max(keys):
        if k in keys:
            print("SEQ:", tocheck, "-", fivedigits[k])
            return True, fivedigits[k], highest
        else:
            print("Skipping", k)
            return False, "", highest
    if k < highest:
        return False, "", highest
    print("Generating", k, tocheck)
    highest = k
    return True, genhash(tocheck), highest

highest = 0
def hasfuturehash(j, charval):
    for k in range(1000):
        tocheck = startcode + str(k+j)

        isvalid, md5, highest = gethash(k+j, tocheck, highest)
        if not isvalid:
            for c in range(0, len(md5) - 5):
                if len(set(md5[c:c + 5])) == 1:
                    fivedigits[k+j] = md5[c]
                    print("5dig:", md5)
                if md5[c] == charval:
                    return True
    return False

#a = "1234567"
#print(a[2:2+2])
#exit()

md5len = len(hashlib.md5(startcode.encode('utf-8')).hexdigest())
i = 0
while count < 65:
    tocheck = startcode + str(i)
    # tocheck = "abc3231929"
    md5 = genhash(tocheck)
    for c in range(0, md5len - 3):
        if len(set(md5[c:c+3])) == 1:
            #if c < md5len - 6 and len(set(md5[c:c+6])) == 1:
            #        break
            #if c < md5len - 5 and len(set(md5[c:c+5])) == 1:
            #        break
            threedigits[i] = md5[c]
            #print(i, md5)
            if hasfuturehash(i+1, md5[c]):
                count += 1
                print(count, i, md5)
            break
#    for c in range(0, md5len - 5):
#        if len(set(md5[c:c + 5])) == 1:
#            d = md5[c]
#            for k in threedigits.keys():
#                if k > i-1000 and threedigits[k] == d:
#                    count += 1
#                    print(count, k, i, threedigits.keys())
#                    break
#            break
    i += 1
    if i == 1000000:
        break

print("Done")