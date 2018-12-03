a,f,u=open('1','r').readlines(),0,0
while 1:
	for s in a:
		u+=int(s.strip())
		if u in f:
			print(u)
			exit()
		f.append(u)