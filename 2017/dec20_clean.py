inp = [l.split() for l in open('20.txt')]

particles = []
for l in inp:
    part = dict()
    for data in l:
        d = data.replace("=<", " ").replace(",", " ").replace(">", "").split()
        part[d[0]] = list(map(int, d[1:]))
        part["np"] = [0,0,0]
    particles.append(part)

for j in range(1, 1000):
    used = []
    newpart = []
    toremove = []
    for i in range(len(particles)):
        part = particles[i]
        for d in range(2):
            part["np"][d] = part["p"][d] + j * part["v"][d] + ((j ** 2 + j) // 2) * part["a"][d]
        if not part["np"] in used:
            used.append(part["np"])
            newpart.append(part)
        else:
            if not part["np"] in toremove:
                toremove.append(part["np"])

    i = 0
    while i < len(newpart):
        for p in toremove:
            if newpart[i]["np"] == p:
                newpart.remove(newpart[i])
        i += 1

    particles = newpart
    print(len(particles))

exit()
