import os

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\1.txt'
fuel = sum([int(_)//3 - 2 for _ in open(filename, 'r').readlines()])

print(f"First challenge: {fuel}")

def fuelreq(mass):
    res = mass // 3 - 2
    f = res
    while f > 0:
        r = f // 3 - 2
        if r <= 0:
            return res
        res += r
        f = r
    

modules = [int(_) for _ in open(filename,'r').readlines()]

fuel = 0
for m in modules:
    fuel += fuelreq(m)

print(f"Second challenge: {fuel}")

print(sum([fuelreq(int(_)) for _ in open(filename,'r').readlines()]))