from collections import defaultdict
all=[ s.strip() for s in open('2','r').readlines()]

def star1():
	c2, c3 = 0,0
	for s in all:
		cnt = defaultdict(int)
		for c in s:
			cnt[c] += 1
		if 2 in cnt.values(): c2 += 1
		if 3 in cnt.values(): c3 += 1
		
	print(c2, c3, c2*c3)

def cdiff(s1, s2):
	r = 0
	for i in range(0, len(s1)):
		if s1[i] != s2[i]:
			r += 1
	return r

def star2():
	for i in range(0, len(all)-1):
		for j in range(i+1, len(all)):
			if cdiff(all[i], all[j]) == 1:
				print(all[i])
				print(all[j])
				exit
			#print(all[j])

star2()