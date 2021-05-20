from timing import timeit
# Actual indata
mine, door = 12092626, 4707356
# Demo indata
# mine, door = 5764801, 17807724

@timeit
def star1():
    res, c = 1, 0
    print("Find loop number for mine")
    while res != mine:
        c += 1
        res = (res * 7) % 20201227
    res = 1
    print("Get encryption key by encrypting the door public key")
    for i in range(c):
        res = (res * door) % 20201227
    print(res)

star1()
exit()
print("===")
my_pk = [1]
door_pk = [1]
maxloop = 20_000_000 # Trimmed down after the fact...

def get_key(n, *, init=1, loop_from=0, subjectnr=7):
    res = init
    for i in range(loop_from, n):
        res *= subjectnr
        res %= 20201227
    return res

for m_loop in range(1, maxloop):
    my_pk.append(get_key(
        m_loop,
        init=my_pk[m_loop-1],
        loop_from=m_loop-1,
        subjectnr=7))
    if m_loop % 1_000_000 == 0:
        print(m_loop)
    if my_pk[m_loop] != mine:
        continue
    for d_loop in range(len(door_pk), maxloop):
        door_pk.append(get_key(
            d_loop,
            init=door_pk[d_loop-1],
            loop_from=d_loop-1,
            subjectnr=7))
        if my_pk[m_loop] == mine and door_pk[d_loop] == door:
            print(f"Found it! ({m_loop} // {d_loop})")

            print(get_key(d_loop, subjectnr=mine))
            #print(get_key2(m_loop, subjectnr=door))
            exit()

print("Not found. Loop higher!")
