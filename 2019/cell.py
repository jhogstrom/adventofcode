class Cell:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def nextmove(self, direction):
        if direction == "U":
            return Cell(self.x, self.y + 1)
        if direction == "D":
            return Cell(self.x, self.y - 1)
        if direction == "R":
            return Cell(self.x + 1, self.y)
        if direction == "L":
            return Cell(self.x - 1, self.y)
        print(f"Cannot move to [{direction}]")

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return hash((self.x, self.y))

    def manhattandist(self, c):
        return abs(self.x - c.x) + abs(self.y - c.y)

    def add(self, x, y):
        return Cell(self.x + x, self.y + y)