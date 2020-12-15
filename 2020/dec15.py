from timing import timeit


data, count, res = "19,0,5,1,10,13", 30000000, 0

# data, count, res = "1,3,2", 2020, 1
# data, count, res = "2,1,3", 2020, 10
# data, count, res = "1,2,3", 2020, 27
# data, count, res = "2,3,1", 2020, 78
# data, count, res = "3,2,1", 2020, 438
# data, count, res = "3,1,2", 2020, 1836

# data, count, res = "0,3,6", 30000000, 175594
# data, count, res = "1,3,2", 30000000, 2578
# data, count, res = "2,1,3", 30000000, 3544142
# data, count, res = "1,2,3", 30000000, 261214
# data, count, res = "2,3,1", 30000000, 6895259
# data, count, res = "3,2,1", 30000000, 18
# data, count, res = "3,1,2", 30000000, 362


# data = {int(_):0 for _ in data.split(",")}

data = [int(_) for _ in data.split(",")]
print(data)

def solution1(n, data):
    """
    Saves all generated numbers in an array.txt
    Every turn, map the array to the indexes of the recent number.
    Calculate the diff between the last two.
    """
    turns = len(data)
    while turns <= n:
        last = data[-1]
        # print(f"{turns}: {last} -- {data}")
        said = [_ for _ in range(len(data)) if data[_] == last]
        # print(said)

        if len(said) == 0:
            # print(f"never spoken {last}")
            data.append(0)
        elif len(said) == 1:
            # print(f"{last} spoken once")
            data.append(0)
        elif len(said) >= 2:
            # print(f"{last} spoken @ {said}")
            data.append(said[-1] - said[-2])
        turns += 1
        # print("---")
    return data[n-1]

@timeit
def solution2(n, data):
    """
    Caches the index of each occurence in a map int -> list
    Cut the  list to save only the two last occurences.
    Calculate the diff between them.
    """
    print(data, len(data), n)
    cache = {data[_]: [_] for _ in range(len(data))}
    display = 1_000_000
    # turns = len(data)
    last = data[-1]
    for turns in range(len(data), n):

        # print(f"Speaking {last}")
        if not last in cache:
            # data.append(0)
            last = 0
            cache[0].append(0)
            continue

        said = cache[last]
        # print(f"{turns+1}: {last} {said} -- {data}")
        if len(said) == 1:
            d = 0
        else:
            d = said[-1] - said[-2]

        # data.append(d)
        last = d
        if d not in cache:
            cache[d] = [turns]
        else:
            cache[d].append(turns)
            cache[d] = cache[d][-2:]

        # print("---")
        # if turns % display == 0:
        #     print(turns//display, len(cache))
    return last

@timeit
def solution3(n, data):
    """
    Store the last occurence of a number in a map int -> int.
    Calculate the diff between the index of last turn and the last occurence for the number.
    """
    # print(data, len(data), n)
    cache = {data[_]: _ for _ in range(len(data)-1)}
    # print(cache)
    # display = 1_000_000
    last = data[-1]
    for turns in range(len(data)-1, n-1):

        # print(f">> {turns}: {last}")
        if last not in cache:
            cache[last] = turns
            # print(f"   First chance to see {last}... {cache}")
            last = 0
            continue

        # # print(f"   Last time was {cache[last]}, {turns - cache[last]} ago")

        cache[last], last = turns, turns - cache[last]

        # print(f"   {cache}")

        # if turns % display == 0:
        #     print(turns//display, len(cache))
    return last


# r = solution2(count, data.copy())
# print(f"{r} == {res}: {r==res}")
# r = solution3(count, data.copy())
# print(f"{r} == {res}: {r==res}")
# exit()


s1 = 2020
s2 = 30_000_000
print(f"* {solution3(s1, data.copy())}")
print(f"** {solution3(s2, data.copy())}")
