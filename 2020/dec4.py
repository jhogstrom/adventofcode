import os
import itertools
import time

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec4.txt'
data = [_.strip() for _ in open(filename, 'r').readlines()]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}

# data = [
#     "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
# "byr:1937 iyr:2017 cid:147 hgt:183cm",
# "",
# "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
# "hcl:#cfa07d byr:1929",
# "",
# "hcl:#ae17e1 iyr:2013",
# "eyr:2024",
# "ecl:brn pid:760753108 byr:1931",
# "hgt:179cm",
# "",
# "hcl:#cfa07d eyr:2025 pid:166559648",
# "iyr:2011 ecl:brn hgt:59in"
# ]

class Passport():
    def __init__(self, s):
        self.fields = {_.split(":")[0]:_.split(":")[1] for _ in s.split()}

    def fields_present(self) -> bool:
        return set(self.fields.keys()) == required_fields \
            or (len(self.fields) == 7 and self.fields.get('cid') is None)

    def validate_byr(self, s) -> bool:
        return 1920 <= int(s) <= 2002

    def validate_iyr(self, s) -> bool:
        return 2010 <= int(s) <= 2020

    def validate_eyr(self, s) -> bool:
        return 2020 <= int(s) <= 2030

    def validate_hgt(self, s) -> bool:
        unit = s[-2:]
        if unit not in ["cm", "in"]:
            return False
        d = int(s[:-2])
        if unit == "cm":
            return 150 <= d <= 193

        if unit == "in":
            return 59 <= d <= 76

        return False

    def validate_hcl(self, s) -> bool:
        return s[0] == "#" and len(s) == 7 and all([_ in "0123456789abcdef" for _ in s[1:]])

    def validate_ecl(self, s) -> bool:
        return s in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def validate_pid(self, s) -> bool:
        return len(s) == 9 and s.isnumeric()

    def validate_cid(self, s) -> bool:
        return True

    def fields_valid(self) -> bool:
        validators = {
            'byr': self.validate_byr,
            'iyr': self.validate_iyr,
            'eyr': self.validate_eyr,
            'hgt': self.validate_hgt,
            'hcl': self.validate_hcl,
            'ecl': self.validate_ecl,
            'pid': self.validate_pid,
            'cid': self.validate_cid,}
        return all(validators[k](self.fields.get(k)) for k in self.fields.keys())

def star1(rec) -> bool:
    p = Passport(rec)
    return p.fields_present()

def star2(rec) -> bool:
    p = Passport(rec)
    return p.fields_present() and p.fields_valid()

def loop_passports(checkvalid):
    s = ""
    count = 0
    rec = ""
    for s in data:
        if s != "":
            rec += " " + s
        else:
            if checkvalid(rec):
                count += 1
            rec = ""

    if checkvalid(rec):
        count += 1


    print(count)

loop_passports(star1)
loop_passports(star2)