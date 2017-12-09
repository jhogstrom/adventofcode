inp = [l.strip() for l in open('8.txt')]
#inp = [
#"b inc 5 if a > 1",
#"a inc 1 if b < 5",
#"c dec -10 if a >= 1",
#"c inc -20 if c == 10",
#]

regs = dict()
highest = 0

def condeval(reg, condition, val):
    rv = 0
    if reg in regs:
        rv = regs[reg]
    if condition == "==": return rv == val
    if condition == ">": return rv > val
    if condition == "<": return rv < val
    if condition == "!=": return rv != val
    if condition == ">=": return rv >= val
    if condition == "<=": return rv <= val
    raise Exception(condition)

def modreg(r, op, v):
    if not r in regs:
        regs[r] = 0
    if op == "inc":
        print("{} INC {}".format(r, v))
        regs[r] += v
    else:
        print("{} DEC {}".format(r, v))
        regs[r] -= v

for l in inp:
    print(l)
    p = l.split(" ")
    r = p[0]
    op = p[1]
    v = int(p[2])
    cr = p[4]
    c = p[5]
    cv = int(p[6])
    if (condeval(cr, c, cv)): modreg(r, op, v)
    highest = max([regs[r], highest])

print(max(regs.values()), highest)
#8022 9819