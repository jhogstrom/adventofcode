k = 6
base = 3
for a in range(2, 10000):
    # print(a)
    for b in range(2, a):
        prev = base**k
        for n in range(2, k):
            r = a**n - b**n - base**k
            # print(a, b, n, r)
            if 0 < r > prev:
                # print("***")
                break
            if r == 0:
                print(f"a={a}, b={b}, n={n}  (k={k})")
                print(f"{a**n} - {b**n} => {a**n-b**n} == {base**k}  -- a-b={a-b}")
                # exit()
            prev = r