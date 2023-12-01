best_year = 27

start_from = 52

y = start_from
experience = 0
value = 1/best_year
while experience < value:
    experience += 1/y
    y += 1
    print(y, experience, "=>", value)

print("Age:", y)