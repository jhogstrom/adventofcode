from collections import defaultdict
all=[ s.strip() for s in open('4s','r').readlines()]

testdata = [
"[1518-11-01 00:00] Guard #10 begins shift",
"[1518-11-01 00:05] falls asleep",
"[1518-11-01 00:25] wakes up",
"[1518-11-01 00:30] falls asleep",
"[1518-11-01 00:55] wakes up",
"[1518-11-01 23:58] Guard #99 begins shift",
"[1518-11-02 00:40] falls asleep",
"[1518-11-02 00:50] wakes up",
"[1518-11-03 00:05] Guard #10 begins shift",
"[1518-11-03 00:24] falls asleep",
"[1518-11-03 00:29] wakes up",
"[1518-11-04 00:02] Guard #99 begins shift",
"[1518-11-04 00:36] falls asleep",
"[1518-11-04 00:46] wakes up",
"[1518-11-05 00:03] Guard #99 begins shift",
"[1518-11-05 00:45] falls asleep",
"[1518-11-05 00:55] wakes up"]

#all = testdata
id = -1

times=defaultdict(list)

# Get all fall asleep events
for s in all:
	d = s[1:11]
	t = int(s[12:17][3:])
	c = s[19:]
	if "Guard" in c: 
		id = int(c.split()[1][1:])
	elif "falls" in s:
		sleepstart = t
	else:
		times[id].append([sleepstart, t])

sleeptimes = defaultdict(int)
sleepminutes = dict()


gmax, sleepmax = 0, 0
for g in times:
	sleepminutes[g] = [0 for _ in range(60)]
	for t in times[g]:
		mstart = t[0]
		mstop = t[1]

		sleeptimes[g] += mstop - mstart
		for m in range(mstart, mstop):
			sleepminutes[g][m] += 1
		if sleeptimes[g] > sleepmax:
			sleepmax = sleeptimes[g]
			gmax = g

sleepmins = defaultdict(int)
mmax = 0
maxminute = -1
for t in times[gmax]:
	mstart = t[0]
	mstop = t[1]
	for m in range(mstart, mstop):
		sleepmins[m] += 1
		if sleepmins[m] > mmax:
			mmax = sleepmins[m];
			maxminute = m

print("ID: {0} Maximum minute: {1} Checksum: {2}".format(gmax, maxminute, gmax * maxminute))

maxminute = 0
maxminuteamount = 0
maxguard = 0
for g in sleepminutes:
	for m in range(len(sleepminutes[g])):
		if sleepminutes[g][m] >= maxminuteamount:
			maxminute = m
			maxguard = g
			maxminuteamount = sleepminutes[g][m]

print("maxsleepmin", "count", maxminuteamount, "guard", maxguard, "minute", maxminute, maxguard * maxminute)