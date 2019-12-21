import os
import itertools
from cell import Cell
import math

curdir = os.path.dirname(os.path.abspath(__file__))

class Asteroids:
    def __init__(self, m):
        self.map = m
        self.visibility_map = []
        self.height = len(m)
        self.width = len(m[0])
        self.asteroids = []
        self.vectors = {}


    def get_vector_set(self, origin, asteroids):
        res = set()
        for a in asteroids:
            if a == origin:
                continue
            dx = origin.x - a.x
            dy = origin.y - a.y
            g = math.gcd(dx, dy)
            res.add((dx // g, dy // g))
        return res

    def get_vectors(self, asteroids):
        return dict((a, self.get_vector_set(a, asteroids)) for a in asteroids)

    def get_astroids_grid(self):
        asteroids = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == "#":
                    asteroids.append(Cell(x, y))
        return asteroids

    def get_angle(self, x, y):
        #angle = math.atan2(x, y) * 180 / math.pi
        #if angle < 0:
        #    angle += 360
        #return angle


        angle = 180 * math.asin(abs(x) / math.sqrt(x**2 + y**2)) / math.pi

        if x >= 0 and y <= 0:
            return angle + 90
        if x < 0 and y <= 0:
            return angle + 180
        if x < 0 and y > 0:
            return angle + 270
        return angle

    def get_angles(self, vectors):
        print("vectors", len(vectors))
        res = {}
        for v in vectors:
            a  = self.get_angle(v[0], v[1])
            if a in res:
                print(v, res[a], a)
            res[a] = v
        r = set(self.get_angle(v[0], v[1]) for v in vectors)
        print("r", len(r))
        
        res = dict((self.get_angle(v[0], v[1]), v) for v in vectors)
        print("angles", len(res))
        return res


    def printarray(self, arr, formspec, detected = None, current = None):
        for y in range(len(arr)):
            for x in range(len(arr[y])):
                s = f"{arr[y][x]:{formspec}}"
                if s.strip() == "0":
                    s = "  ."
                if detected and Cell(x, y) in detected:
                    s = "O"
                if current and Cell(x, y) == current:
                    s = "X"
                print(s, end = "")
            print()
        print("===")

    def visualize(self):
        self.printarray(self.visibility_map, ">3")

    def print_asteroids(self):
        self.printarray(self.map, "1")


def star1():
    filename = f'{curdir}\\dec10.txt'
    data = [l.strip() for l in open(filename, 'r').readlines()]
    a = Asteroids(data)
    asteroids = a.get_astroids_grid()
    vectors = a.get_vectors(asteroids)

    max_visibility = max([len(vectors[_]) for _ in vectors])
    print(f"Star1: {max_visibility}")

def star2():
    filename = f'{curdir}\\dec10.txt'
    data = [l.strip() for l in open(filename, 'r').readlines()]
    a = Asteroids(data)
    asteroids = a.get_astroids_grid()
    vectors = a.get_vectors(asteroids)
    max_visibility = max([len(vectors[_]) for _ in vectors])
    origin = [_ for _ in vectors if len(vectors[_]) == max_visibility][0]
    angles = a.get_angles(vectors[origin])
    for a in sorted(angles.keys()):
        print(a, angles[a])
    print(len(vectors[origin]))
    print(len(angles))
    a = sorted(angles.keys())[200]
    v = angles[a]
    current_cell = origin.add(v[0], v[1])
    print(origin, v)
    c = 0
    while current_cell not in asteroids:
        current_cell = current_cell.add(v[0], v[1])
        print(f"Moving to {current_cell}")
        c += 1
        if c > 250:
            print("Something went wrong")
            break
    print(a, angles[a], origin, current_cell)
    print(f"answer: {current_cell.x * 100 + current_cell.y}")
    print("312 is too low")
    print("1415 is too high")

star1()
star2()