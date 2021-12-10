from shutil import copyfile
import os
import sys


def copy(src, year, day):
    dest = os.path.os.path.basename(src.replace("XX", day))
    dest = f"{year}/{dest}"

    if os.path.exists(dest):
        print(f"Unable to copy over {dest}")
        return
    copyfile(src, dest)

day = sys.argv[1]
year = "2021"
curdir = os.path.dirname(os.path.abspath(__file__))

copy(f"{curdir}/templates/decXX.py", year, day)
copy(f"{curdir}/templates/decXX.txt", year, day)
copy(f"{curdir}/templates/decXX_test.txt", year, day)
