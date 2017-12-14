from collections import defaultdict

inp = open('13.txt').readlines()
#print(inp)

def initfw():
    scanpos = defaultdict(int)
    direction = defaultdict(bool)
    fw = defaultdict(int)
    for l in inp:
        layer, depth = map(int, l.split(":"))
        fw[layer] = depth
    return fw, direction, scanpos

def movescanners():
    for p in fw:
        if fw[p] == 0:
            continue
        turn = False
        newp = scanpos[p]
        if direction[p]:
            newp += 1
            if newp >= fw[p]:
                turn = True
                newp -= 2
        else:
            newp -= 1
            if newp < 0:
                turn = True
                newp += 2
        if turn:
            #            print("Turning on {} ({})- {}".format(p, newp, direction[p]))
            direction[p] = not direction[p]
        if fw[p] != 0:
            scanpos[p] = newp


def runpackage():
    severity = 0
    for i in range(max(fw) + 1):
    #    print("scanning {} - {} [{}]".format(i, scanpos[i], scanpos))
        if fw[i] != 0 and scanpos[i] == 0:
#            print("Caught@[{}] - {}".format(i, scanpos[i]))
            severity += i * fw[i]
        movescanners()
    return severity


#fw, direction, scanpos = initfw()
#print(runpackage())

#fw, direction, scanpos = initfw()
#movescanners()
#movescanners()
#movescanners()
#print(runpackage())

#exit()


delay  = 0
while 1:
    fw, direction, scanpos = initfw()
    for d in range(delay):
        movescanners()
    cost = runpackage()
    print("Delay: {} - Cost: {}".format(delay, cost))
    if not cost:
        break
    delay += 1
#    if delay > 30: break

