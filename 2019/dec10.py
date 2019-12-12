import os
import itertools

curdir = os.path.dirname(os.path.abspath(__file__))

class Asteroids:
    def __init__(self, m):
        self.map = m
        self.visibility_map = []
        self.height = len(m)
        self.width = len(m[0])

    def scan_vector(self, x, y, deltax, deltay):
 #       print(f"==={x},{y} - {deltax},{deltay}")
        while x + deltax in range(self.width) and y + deltay in range(self.height):
            x += deltax
            y += deltay
            if self.map[y][x] == "#":
 #               print(x, y)
                return True
        return False

    def scan_pos(self, x, y):
        print(f"Scanning {x}, {y}")
        # north-east quadrant
        res = 0
        for deltax in range(0, self.width-x):
            for deltay in range(1, y+1):
#                print(f">>{x},{y} Delta: {deltax}, {-deltay}")
                if self.scan_vector(x, y, deltax, -deltay):
                    res += 1
        return res

    def scanmap(self):
        self.visibility_map = []
        for y in range(len(self.map)):
            row = []
            for x in range(len(self.map[y])):
                if self.map[y][x] == "#":
                    row.append(self.scan_pos(x, y))
                else:
                    row.append(0)
            self.visibility_map.append(row)

    def printarray(self, arr, formspec):
        for y in range(len(arr)):
            r = ""
            for x in range(len(arr[y])):
                r += f"{arr[y][x]:{formspec}}"
            print(r)

    def visualize(self):
        self.printarray(self.visibility_map, "<2")

    def print_asteroids(self):
        self.printarray(self.map, "1")

    def getmax(self):
        max_by_row = []
        for y in range(len(self.visibility_map)):
            scanline = [_ for _ in self.visibility_map[y] if isinstance(_, int)]
            if len(scanline) > 0:
                max_by_row.append(max(scanline))
        return max(max_by_row)

def dec10_2():
    filename = f'{curdir}\\dec10.txt'
    data = [l.strip() for l in open(filename, 'r').readlines()]

    data = [".#..#",
            ".....",
            "#####",
            "....#",
            "...##"]
    a = Asteroids(data)
#    a.scanmap()
    a.print_asteroids()
    a.visualize()
#    print(a.scan_pos(3, 4))
    print(a.getmax())


dec10_2()