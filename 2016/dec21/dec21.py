lines = [ l.strip() for l in open('dec21.txt', 'r').readlines()]




def reversepos(s, rfrom, rto):
    return s[:rfrom] + s[rfrom:rto+1][::-1] + s[rto+1:]

def swappos(s, sfrom, sto):
    return s[:sfrom] + s[sto:sto+1] + s[sfrom+1:sto] + s[sfrom:sfrom+1] + s[sto+1:]

def movepos(s, mfrom, mto):
    s = list(s)
    s[mto] = s[mfrom]
    if mfrom < mto:
        s.remove(mfrom)
    else:
        s.remove(mfrom - 1)
    return str(s)
    if mfrom > mto:
        return s[:mto] + s[mfrom:mfrom+1] + s[mto:mfrom] + s[mfrom+1:]
    return s[:mfrom-1] #+ s[mfrom+1:mto] + s[mfrom:mfrom+1] + s[mto:]


print(reversepos("12345", 0, 1))
print(swappos("12345", 2, 4))
print(movepos("12345", 0, 3))
exit()

s = "abcdefgh"



for l in lines:
    p = l.split(" ")
    if l.startswith("reverse positions"): #reverse positions 1 through 6
        s = reversepos(s, int(p[2]), int(p[4]))
        continue
    if l.startswith("swap position "): #swap position 4 with position 1
        s = swappos(s, int(p[2]), int(p[5]))
        continue
    if l.startswith("move position"): #move position 5 to position 7
        s = movepos(p, int(p[2]), int(p[5]))




