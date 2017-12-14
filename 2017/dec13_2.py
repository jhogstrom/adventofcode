from collections import defaultdict
inp = open('13ex.txt').readlines()

def init():
    fw = defaultdict(int)
    hit = defaultdict(int)
    for l in inp:
        layer, depth = map(int, l.split(":"))
        fw[layer] = depth
        hit[layer] = 2 * depth - 1
    return fw, hit

m=0

while 1:
    severity = 0
    fw, hit = init()
    for i in fw:
        if (i+m) % (hit[i]-1) == 0:
            #severity += i * fw[i]
            #print("Caught@[{}] - {}->{}".format(i, hit[i], fw[i]))
            severity += 1
    if m % 1000 == 0:
        print("Round", severity, m)
    if severity == 0: break
    m += 1

print(severity, m)

print("round should be larger than 171428")