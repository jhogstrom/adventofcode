import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.clock()
        result = method(*args, **kw)
        te = time.clock()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            name = f'{method.__name__}{args}'[:50]
            duration_ms = (te - ts)*1000
            if duration_ms < 1:
                print(f'{name}: {int(duration_ms*1000)}us')
            elif duration_ms < 1000:
                print(f'{name}: {duration_ms:2.3f}ms')
            else:
                print(f'{name}: {duration_ms/1000:2.2f}s')
        return result
    return timed