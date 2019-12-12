from collections import defaultdict

pwd_lo, pwd_hi = 108457, 562041

def isvalid(nums):
    # Numbers increasing
    if nums[0] > nums[1] or nums[1] > nums[2] or \
        nums[2] > nums[3] or nums[3] > nums[4] or nums[4] > nums[5]:
        return False

    # count how many of each number
    groups = defaultdict(int)
    for n in nums:
        groups[n] += 1
    # Should be at least one pair
    return any([groups[_] == 2 for _ in groups])

print(len([n for n in range(pwd_lo, pwd_hi) if isvalid([int(_) for _ in str(n)])]))

def check(n):
    print(f"{n} -- {isvalid([int(_) for _ in str(n)])}")

def dochecks():
    check(111122)
    check(111222)
    check(111111)
    check(113344)
    check(111112)
    check(122222)
    check(111234)
    check(122234)
    check(123334)
    check(123444)
    check(112222)
    check(557899)
    exit()

#dochecks()
