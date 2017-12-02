import hashlib
from symbol import while_stmt

startcode = "ffykfhsq"
password = [" ", " ", " ", " ", " ", " ", " ", " "]
pcount = 0
i = 0
while pcount < 8:
    tocheck = startcode + str(i)
    #tocheck = "abc3231929"
    md5 = hashlib.md5(tocheck.encode('utf-8')).hexdigest()
    #print(i, password, md5[0:5], md5[5], md5, tocheck)
    if md5[0:5] == "00000" and md5[5] in "01234567":
        pos = int(md5[5])
        if password[pos] == " ":
            password[pos] = md5[6]
            print(password)
            pcount += 1
    i += 1
    #
    # if i % 100000 == 0: print(i)
    #break

print(password, "done")
print(str(password))