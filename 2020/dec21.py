import helpers
from itertools import permutations
from collections import defaultdict

data = helpers.get_data(__file__)

# data = [
# "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
# "trh fvjkl sbzzf mxmxvkd (contains dairy)",
# "sqjhc fvjkl (contains soy)",
# "sqjhc mxmxvkd sbzzf (contains fish)",
# ]


def printdict(title, d):
    print(f"\n{title}")
    for k, v in d.items():
        print(f"{k}: {v}")

def parse(s):
    ingredients, allergens = d.split(" (contains ")
    ingredients = set(ingredients.split())
    allergens = set(allergens[:-1].split(", "))
    return ingredients, allergens

food_with_allergen = defaultdict(set)
appearance = defaultdict(int)
all_allergens = set()
all_ingredients = set()


# find the sets of all ingredients and allergens
for d in data:
    ingredients, allergens = parse(d)
    all_ingredients |= ingredients
    all_allergens |= allergens

# prime the list
# for a in all_allergens:
#     food_with_allergen[a] = all_ingredients.copy()

for d in data:
    ingredients, allergens = parse(d)
    for a in allergens:
        food_with_allergen[a] |= ingredients

    for i in ingredients:
        appearance[i] += 1

contains_allergens = set()
for f in food_with_allergen.values():
    contains_allergens |= f

no_allergens = all_ingredients - contains_allergens

res = 0
for n in no_allergens:
    res += appearance[n]

print(f"* {res}")

canonical_list = {}
while food_with_allergen:
    unique = {k:v for k, v in food_with_allergen.items() if len(v) == 1}
    # printdict("unique", unique)
    for k, v in unique.items():
        canonical_list[k] = list(v)[0]
        for m in food_with_allergen:
            food_with_allergen[m] = food_with_allergen[m] - v

    food_with_allergen = {k:v for k,v in food_with_allergen.items() if v}

# printdict("canonical_list", canonical_list)

r = ",".join([canonical_list[k] for k in sorted(canonical_list)])
print(f"** {r}")


