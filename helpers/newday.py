import argparse
import os


def copy(src, year, day):
    dest = os.path.basename(src.replace("XX", day))
    dest = f"{year}/{dest}"

    if os.path.exists(dest):
        print(f"Unable to copy over {dest}")
        return
    x = open(src).read()
    x = x.replace('"X"', f'"{day}"')
    x = x.replace('"XX"', f'"{day}"')
    x = x.replace("YEAR", f"{year}")
    open(dest, "w").write(x)


parser = argparse.ArgumentParser(
    description="Copy template files for a specific day and year."
)
parser.add_argument("--day", required=True, help="Day of the month")
parser.add_argument("--year", required=True, help="Year")

args = parser.parse_args()
year = args.year
day = args.day

curdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

copy(f"{curdir}/templates/decXX.py", year, day)
# copy(f"{curdir}/templates/decXX.txt", year, day)
copy(f"{curdir}/templates/decXX_test.txt", year, day)
