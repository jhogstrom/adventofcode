inp = open('9.txt').readline()
#inp = "{}" # 1
#inp = "{{{}}}" #6.
#inp = "{{},{}}" #score of 1 + 2 + 2 = 5.
#inp = "{{{},{},{{}}}}" # score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
#inp = "{<a>,<a>,<a>,<a>}" # score of 1.
#inp = "{{<ab>},{<ab>},{<ab>},{<ab>}}" # score of 1 + 2 + 2 + 2 + 2 = 9.
#inp = "{{<!!>},{<!!>},{<!!>},{<!!>}}" # score of 1 + 2 + 2 + 2 + 2 = 9.
#inp = "{{<a!>},{<a!>},{<a!>},{<ab>}}" # score of 1 + 2 = 3.

#inp = "<>" # 0 characters.
#inp = "<random characters>" # 17 characters.
#inp = "<<<<>" # 3 characters.
#inp = "<{!>}>" # 2 characters.
#inp = "<!!>" # 0 characters.
#inp = "<!!!>>" # 0 characters.
#inp = '<{o"i!a,<{i<a>' # 10 characters.

def codegolf():
    d = open('9').readline()
    i = g = gc = xc = 0
    x = False
    while i < len(d):
        c = d[i]
        if c == "!": i += 2;continue
        if c == "<":
            if x: xc += 1
            x = True
        elif c == ">":
            x = False
        elif not x and c == "{":
            g += 1
        elif not x and c == "}":
            gc += g;g -= 1
        elif x:
            xc += 1
        i += 1
    print(gc, xc)

def solution():
    i = 0
    group = 0
    garbage = False
    gc = 0
    garb = 0
    while i < len(inp):
        c = inp[i]
        if c == "!":
            i+= 2
            continue
    #    print(c)
        if c == "<":
            if garbage:
                garb += 1
            garbage = True
    #        print("garbage", garbage)
        elif c == ">":
            garbage = False
            #print("garbage", garbage)
        elif not garbage and c == "{":
            group += 1
        elif not garbage and c == "}":
            gc += group
            group -= 1
        elif garbage:
            garb += 1

        i += 1

    #11898
    # > 4506

    print(gc, garb)

solution()