import logging
import os


levels = {
    True: logging.DEBUG,
    False: logging.INFO
}


def get_data(stardate, runtest):
    logging.basicConfig(level=levels[runtest], format="%(message)s")
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
