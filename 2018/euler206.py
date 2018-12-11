import math  

#1_2_3_4_5_6_7_8_9_0
maxnum = 1929394959697989900
minnum = 1020304050607080900
print(math.sqrt(maxnum))
print(math.sqrt(minnum))
print(math.sqrt(100000000000000))
#exit()

#print("1020304050607080900"[::2])
#exit()
minstart = int(math.sqrt(minnum))
print(minstart)

c = 0
i = 1389018730
i = int(math.sqrt(minnum)) + 20
i3 = True
while i < math.sqrt(maxnum):
	r = str(i**2)
	n = r[::2]
	if n == "1234567890":
		print("=>", r, i)
		exit()
	print(i**2, i)
	if i3:
		i += 40
	else:
		i += 60
	i3 = not i3
	if n[1] != "2":
		i += 1000000
	elif n[2] != "3":
		i += 10000
#	if n[2] != "4":
#		i += 100 
	c += 1
	if c % 10000 == 0:
		print(r)
