discs = [
    [13, 10],
    [17, 15],
    [19, 17],
    [7, 1],
    [5, 0],
    [3, 1],
    [11, 0]
]

#discs = [
#    [5, 4],
#    [2, 1]
#]

t = 0

drange = range(len(discs))
while True:
    done = True
    for i in drange:
        if (discs[i][1] + t + i + 1) % discs[i][0] != 0:
            done = False
            break
    if done:
        print("Done at:", t)
        break
    t += 1
    if t % 1000 == 0:
        print("t", t)

