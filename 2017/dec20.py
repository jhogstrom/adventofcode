from collections import defaultdict

inp = [l.split() for l in open('20.txt')]
print(inp)

particles = []
for l in inp:
    part = dict()
    for data in l:
        d = data.replace("=<", " ").replace(",", " ").replace(">", "").split()
        part[d[0]] = list(map(int, d[1:]))
    particles.append(part)


j = 0
while 1:
    j += 1
    used = []
    newpart = []
    toremove = []
    for i in range(len(particles)):
        part = particles[i]
        for d in range(2):
            part["v"][d] += part["a"][d]
            part["p"][d] += part["v"][d]
        if not part["p"] in used:
            used.append(part["p"])
            newpart.append(part)
        else:
            print("Eliminating", i, part["p"], toremove)
            ix = used.index(part["p"])
            if not ix in toremove:
                toremove.append(ix)

    toremove = sorted(toremove)[::-1]
    #print("to remove:", toremove)
    #print("Before removal", len(newpart), newpart)
    for i in toremove:
        newpart = newpart[:i] + newpart[i+1:]
    #print("After removal", len(newpart), newpart)

    particles = newpart

#    print(j, len(particles))
    if j % 1000 == 0: print("remaining @{}: {}".format(j, len(particles)))
#    if j == 5000: break


print("answer" ,len(particles), particles)
