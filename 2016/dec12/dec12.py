lines = [ l.strip() for l in open('dec12.txt', 'r').readlines()]

registers = {c:0 for c in "abcd"}
registers["c"]  = 1
c = 0
pointer = 0
while True:
    if pointer >= len(lines):
        break
    l = lines[pointer]
    parts = l.split(" ")
    cmd = parts[0]
    args = parts[1:]
    c += 1
    if c % 100000 == 0:
        print(c, registers, pointer, l)
        #c = 1

    if cmd == "cpy":
        v, targetreg = args
        if (v.isalpha()):
            registers[targetreg] = registers[v]
        else:
            registers[targetreg] = int(v)
        pointer += 1
        continue
    if cmd == "dec":
        registers[args[0]] -= 1
        pointer += 1
        continue
    if cmd == "inc":
        registers[args[0]] += 1
        pointer += 1
        continue
    if cmd == "jnz":
        v, offset = args
        if v.isalpha():
            if registers[v] != 0:
                pointer += int(offset)
            else:
                pointer += 1
            continue
        if int(v) != 0:
            pointer += int(offset)
        else:
            pointer += 1
            continue


print("a", registers["a"])