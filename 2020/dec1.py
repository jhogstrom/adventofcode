import os
import itertools
import time
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec1.txt'
data = [int(_) for _ in open(filename, 'r').readlines()]

# data = [
#     1721,
#     979,
#     366,
#     299,
#     675,
#     1456]

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

@timeit
def star1():
    complements = [2020 - _ for _ in data]
    res = [_ for _ in data if _ in complements]
    print(res[0] * res[1])

@timeit
def star2():
    print([_ for _ in itertools.product(data, data, data) if sum(_) == 2020])
    for trip in itertools.product(data, data, data):
        if sum(trip) == 2020:
            t = list(trip)
            print(t[0] * t[1] * t[2])
            return
    raise ValueError

star1()
star2()