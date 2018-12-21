number = 10551354
#number = 954
divisors = []
for i in range(1, number+1):
	if number % i == 0:
		print(i)
		divisors.append(i)

print("divisors:", divisors)
print("Sum", sum(divisors))