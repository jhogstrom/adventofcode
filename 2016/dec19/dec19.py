elfcount = 3017957

elfs = [1 for x in range(elfcount)]

#print(elfs)



def nextelf(ix):
    ix += 1
    if ix >= elfcount: ix = 0
    while elfs[ix] == 0:
        ix += 1
        if ix >= elfcount: ix = 0
    return ix

i = 0
c = 0
while c < elfcount - 1:
    c += 1
    takefrom = nextelf(i)
    #print(takefrom)
    elfs[takefrom] = 0
    i = nextelf(takefrom)
    #print(c, elfs)
    if c % 10000 == 0:
        print(c)


print(i+1)