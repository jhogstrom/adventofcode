allinput = [l.strip() for l in open('dec04_input.txt', 'r').readlines()]

st=sorted
validcount = 0
for l in allinput:
    words = []
    isvalid = 1
    for w in l.split(" "):
        sortedw = list(st(w))
        if sortedw in words:
            isvalid = 0
            continue
        words.append(sortedw)
    validcount += isvalid

print(validcount)
