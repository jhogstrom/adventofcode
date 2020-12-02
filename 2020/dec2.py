import os
import itertools
import time
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\dec2.txt'
data = open(filename, 'r').readlines()

# data = [
#     "1-3 a: abcde",
#     "1-3 b: cdefg",
#     "2-9 c: ccccccccc"]

class Checker():
    def __init__(self, s):
        parts = s.split()
        self.range = [int(_) for _ in parts[0].split("-")]
        self.ch = parts[1][0]
        self.pwd = parts[2]

    def __repr__(self):
        return f"{self.range} - {self.ch} -> {self.pwd}"

    def check(self):
        count = len([_ for _ in self.pwd if _ == self.ch])
        return self.range[0] <= count <= self.range[1]

    def check2(self):
        return (self.pwd[self.range[0]-1] == self.ch) ^ (self.pwd[self.range[1]-1] == self.ch)


data = [Checker(_) for _ in data]

def star1():
    print(len([_ for _ in data if _.check()]))


def star2():
    print(len([_ for _ in data if _.check2()]))

star1()
star2()