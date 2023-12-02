import logging
import os
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


def get_data(stardate, runtest: bool):
    if runtest:
        dataname = f"dec{stardate}_test.txt"
        logging.error("USING TESTDATA")
    else:
        dataname = f"dec{stardate}.txt"
    curdir = os.path.dirname(os.path.abspath(__file__))
    filename = f'{curdir}\\{dataname}'
    data = [_.strip() for _ in open(filename, 'r').readlines()]
    if not data:
        raise FileNotFoundError(f"No data in {dataname}")
    return data


def set_logging(showlog: bool):
    levels = {
        True: logging.DEBUG,
        False: logging.INFO
    }
    logging.basicConfig(level=levels[showlog], format="%(message)s")
