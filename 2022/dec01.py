import os

stardate = "01"
dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
data.append("")
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


calories = []
cal = 0
for _ in data:
    if _:
        cal += int(_)
    else:
        calories.append(cal)
        cal = 0
    
print(max(calories))

print(sum(sorted(calories)[-3:]))