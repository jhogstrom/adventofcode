inp = ".^^.^.^^^^"
inp = ".^^^^^.^^^..^^^^^...^.^..^^^.^^....^.^...^^^...^^^^..^...^...^^.^.^.......^..^^...^.^.^^..^^^^^...^."
inp = "." + inp + "."

rows = 400000
room = [inp]

r = 0
while r < rows - 1:
    r += 1
    nextrow = "."
    prev = room[len(room)-1]
    for i in range(1, len(prev) - 1):
        if prev[i-1] == "^" and prev[i] == "^" and prev[i+1] == ".":
            nextrow += "^"
            continue
        if prev[i-1] == "." and prev[i] == "^" and prev[i+1] == "^":
            nextrow += "^"
            continue
        if prev[i - 1] == "^" and prev[i] == "." and prev[i + 1] == ".":
            nextrow += "^"
            continue
        if prev[i - 1] == "." and prev[i] == "." and prev[i + 1] == "^":
            nextrow += "^"
            continue
        nextrow += "."

    nextrow = nextrow + "."
    room.append(nextrow)

totsafe = 0
for r in room:
    safe = sum([1 if x == "." else 0 for x in r]) - 2
    #print(r, safe)
    totsafe += safe

print(totsafe)