oneline = "A(1x5)BC"
#line = "(3x3)XYZ"
oneline = "A(2x2)BCD(2x2)EFG"
oneline = [ l.strip() for l in open('dec09.txt', 'r').readline()]

def expandstring(repeatcount, line):
    rescount = 0
    i = 0
    res = ""
    while i < len(line):
        if line[i] != "(":
            res += line[i]
            i += 1
            rescount += 1
            continue
        cmd = ""
        while line[i] != ")":
            i+=1
            cmd += line[i]
        cmd = cmd[0:-1]
        length, cnt = [ int(s) for s in cmd.split("x")]
        rep = line[i+1:i+length+1]
        #rescount += length * cnt
        rescount += expandstring(cnt, rep)
        #print(cmd, cnt, length, rep)
        #for j in range(cnt):
        #    for k in rep:
        #        res += k

        i += length+1
    return rescount * repeatcount

#    print(res)


print(expandstring(1, oneline))