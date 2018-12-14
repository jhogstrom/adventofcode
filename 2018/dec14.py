inp = "37"

elves = [0, 1]
recipes = [int(_) for _ in inp]

star = 1
star = 2

def makenewrecipes2(recipes):
	return recipes + str(int(recipes[elves[0]]) + int(recipes[elves[1]]))

def targetfound():
	tail = recipes[-len(target):]
	s = ""
	for i in range(len(tail)):
		if target[i] != str(tail[i]):
			return
	print("Recipes before \"{0}\" => {1}".format(target, len(recipes)-len(target)))
	exit()

def makenewrecipes():
	newnum = str(recipes[elves[0]] + recipes[elves[1]])
	for n in newnum:
		recipes.append(int(n))
		if star == 2:
			targetfound()

def moveelves(recipes):
	for e in range(len(elves)):
		elves[e] += ((recipes[elves[e]]) + 1)
		elves[e] %= len(recipes)

def printrecipes(recipes):
	s = ""
	for i in range(len(recipes)):
		if i == elves[0]: fstr = "({0})"
		elif i == elves[1]: fstr = "[{0}]"
		else: fstr = " {0} "
		s += fstr.format(recipes[i])
	print(s)

def oneround(recipes):
	makenewrecipes()
	moveelves(recipes)
	return recipes


iter = 793061
#iter = 2018
target = "51589"
target = "01245"
#target = "9251071"
#target = "59414"
#target = "793061"


if star == 2:
	print("Chasing star2")
	i = 0
	while True:	
		recipes = oneround(recipes)
		printrecipes(recipes)
		i += 1
		if i % 100000 == 0: print(i)
	exit()

if star == 1:
	while len(recipes) < iter + 10:
		recipes = oneround(recipes)
		#printrecipes(recipes)
	s = ""
	for r in recipes[iter:iter+10]:
		s += str(r)
	print("Answer {0}: {1}".format(iter, s))