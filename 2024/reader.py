import argparse
import datetime
import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def ensure_data(dataname, stardate, year: int = None):
    """
    Download test data from adventofcode.com if the file is not already present locally.

    Args:
        dataname (_type_): _description_
        stardate (_type_): _description_
    """

    if year is None:
        year = datetime.datetime.now().year
    filename = f"{year}/{dataname}"

    if not os.path.exists(filename):
        logging.info(f"Downloading {filename}...")
        url = f"https://adventofcode.com/{year}/day/{int(str(stardate))}/input"
        cookies = {"session": os.environ.get("AOC_SESSION")}
        r = requests.get(url, cookies=cookies)
        if r.status_code == 200:
            open(filename, "w").write(r.text)
            logging.info(f"Downloaded {filename}")
        else:
            logging.info(
                f"Unable to download {filename} from '{url}'. Status code: {r.status_code}"
            )
            logging.error(r.text)
            sys.exit(1)


def get_data(stardate, year, runtest: bool, testnum=""):
    if runtest:
        dataname = f"dec{stardate}_test{testnum}.txt"
        logging.error("USING TESTDATA")
    else:
        dataname = f"dec{stardate}.txt"
        ensure_data(dataname, stardate, year)
    curdir = os.path.dirname(os.path.abspath(__file__))
    filename = f"{curdir}\\{dataname}"
    data = [_.strip() for _ in open(filename, "r").readlines()]
    if not data:
        raise FileNotFoundError(f"No data in {dataname}")
    return data


def set_logging(showlog: bool):
    levels = {True: logging.DEBUG, False: logging.INFO}
    logging.basicConfig(level=levels[showlog], format="%(message)s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Year of the advent of code challenge")
    parser.add_argument("--day", help="Day of the advent of code challenge")
    args = parser.parse_args()
    year = args.year
    day = args.day
    get_data(day, year, False)
