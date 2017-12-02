import hashlib
from symbol import while_stmt

salt = "abc"
#salt= "zpqevtbw"

md5len = len(hashlib.md5(salt.encode('utf-8')).hexdigest())

hashes = dict()
keys = []
i = 0
maxcalc = -1

def genhash(ix):
    md5 = salt + str(ix)
    for i in range(2017):
        md5 = hashlib.md5(md5.encode('utf-8')).hexdigest()
    maxcalc = ix
    return md5


def hasthree(ix):
    if hashes.get(i, False) != False:
        return True

    if i < maxcalc:
        return False

    md5 = genhash(ix)
    for c in range(0, md5len - 3):
        if len(set(md5[c:c+3])) == 1:
            hashes[ix] = [md5[c], 0]
            return True


def hasfuture(ix, ch):
    for j in range(ix, 1000):
        if 
        if hasfive()


while len(keys) < 64:
    if hasthree(i):
        if hasfuture(i+1, hashes[i][0]):
            keys.append(i)




