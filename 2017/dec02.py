allinput = open('dec02_input.txt', 'r').readlines()

def star1():
    checksum = 0
    for l in allinput:
        nums = [int(t) for t in l.strip().split("\t")]
        checksum += max(nums) - min(nums)

    print(checksum)

def star2():
    checksum = 0
    for l in allinput:
        nums = sorted([int(t) for t in l.strip().split("\t")])
        print(nums)
        for i in range(len(nums)-1):
            for j in range(i+1, len(nums)):
                if nums[j] % nums[i] == 0:
                    checksum += nums[j]//nums[i]
                    #print(nums[i], nums[j],nums[j]//nums[i] )

    print(checksum)


star2()