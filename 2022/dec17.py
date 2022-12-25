from collections import defaultdict
import os

runtest = False
stardate = 17
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()

data = data[0]


class Coord():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def can_move(self, d, used_space) -> bool:
        if self.x + d < 0:
            return False

        if self.x + d > 6:
            return False

        target = Coord(self.x+d, self.y)
        return target not in used_space

    def can_move_down(self, used_space) -> bool:
        target = Coord(self.x, self.y - 1)
        return target not in used_space


class Rock():
    def __init__(self) -> None:
        self.rocks = []

    def __str__(self) -> str:
        return " - ".join(str(_) for _ in self.rocks)

    def add_piece(self, c):
        self.rocks.append(c)

    def move_sideways(self, d):
        for _ in self.rocks:
            _.x += d

    def copy(self):
        res = Rock()
        for _ in self.rocks:
            res.add_piece(Coord(_.x, _.y))
        return res

    def set_starty(self, y):
        for _ in self.rocks:
            _.y += y

    def move(self, d, used_space):
        if all(_.can_move(d, used_space) for _ in self.rocks):
            for _ in self.rocks:
                _.x += d

    def down(self, used_space):
        if all(_.can_move_down(used_space) for _ in self.rocks):
            for _ in self.rocks:
                _.y -= 1
            return True
        return False


def init_shapes():
    res = []
    # xxxx
    rock = Rock()
    rock.add_piece(Coord(0, 0))
    rock.add_piece(Coord(1, 0))
    rock.add_piece(Coord(2, 0))
    rock.add_piece(Coord(3, 0))
    res.append(rock)

    #  x
    # xxx
    #  x
    rock = Rock()
    rock.add_piece(Coord(1, 2))
    rock.add_piece(Coord(0, 1))
    rock.add_piece(Coord(1, 1))
    rock.add_piece(Coord(2, 1))
    rock.add_piece(Coord(1, 0))
    res.append(rock)

    #   x
    #   x
    # xxx
    rock = Rock()
    rock.add_piece(Coord(2, 2))
    rock.add_piece(Coord(2, 1))
    rock.add_piece(Coord(0, 0))
    rock.add_piece(Coord(1, 0))
    rock.add_piece(Coord(2, 0))
    res.append(rock)

    # x
    # x
    # x
    # x
    rock = Rock()
    rock.add_piece(Coord(0, 3))
    rock.add_piece(Coord(0, 2))
    rock.add_piece(Coord(0, 1))
    rock.add_piece(Coord(0, 0))
    res.append(rock)

    # xx
    # xx
    rock = Rock()
    rock.add_piece(Coord(0, 1))
    rock.add_piece(Coord(1, 1))
    rock.add_piece(Coord(0, 0))
    rock.add_piece(Coord(1, 0))
    res.append(rock)

    for _ in res:
        _.move_sideways(2)

    return res


direction = {
    '<': -1,
    '>': 1
}


def print_well(used_space):
    used_space = sorted(used_space, key=lambda c: c.y)
    maxy = used_space[-1].y
    res = []
    TOPLINE = 10
    for _ in range(maxy - TOPLINE, maxy+1):
        w = [">"] + [' '] * 7 + ["<"]
        res.append(w)
    for _ in res[::-1]:
        print("".join(_))
    for _ in used_space:
        if maxy - _.y < TOPLINE:
            res[maxy - _.y][_.x+1] = "#"
    for i, _ in enumerate(res, maxy-TOPLINE):
        print("".join(_), i)
    print("----")


def star1():
    shapes = init_shapes()
    used_space = set(Coord(x, 0) for x in range(7))
    wind = 0
    ITERATIONS = 2022
    max_y = 4  # Start with three blank lines
    for _ in range(ITERATIONS):
        shape = shapes[_ % len(shapes)].copy()
        start_y = max_y
        shape.set_starty(start_y)
        while True:
            d = data[wind % len(data)]
            wind += 1
            shape.move(direction[d], used_space)
            if not shape.down(used_space):
                break
        used_space = used_space.union(set(shape.rocks))
        max_y = max([max_y] + [_.y + 4 for _ in shape.rocks])

    wmax = max(_.y for _ in used_space)

    return wmax


def star2():
    shapes = init_shapes()
    used_space = set(Coord(x, 0) for x in range(7))
    wind = count = 0
    FREELINES = 4  # Start 4 above ground or highest block.
    max_y = FREELINES
    level_fill = defaultdict(int)
    # lastround = 0
    # seen = False
    # last_height_127 = 0
    # last_round_127 = 0
    MAX = 1_000_000_000_000
    iterations_before_stabilization = 1511  # rounds before stabilization
    cycle_length = 1715  # length of a stable cycle - 1715
    cycle_height = 2574  # how much the tower builds during a cycle of iterlen rounds
    final_rounds = (MAX - iterations_before_stabilization) % cycle_length
    CYCLES = iterations_before_stabilization + final_rounds

    while count < CYCLES:
        shape_index = count % len(shapes)
        shape = shapes[shape_index].copy()
        count += 1
        shape.set_starty(max_y)
        while True:
            d = data[wind % len(data)]
            wind += 1
            shape.move(direction[d], used_space)
            if not shape.down(used_space):
                break
        used_space = used_space.union(set(shape.rocks))
        max_y = max([max_y] + [_.y + FREELINES for _ in shape.rocks])
        for r in shape.rocks:
            level_fill[r.y] += 1

        # Remove all lines below the highest line that is completely full.
        top_level = 0
        for level in range(len(level_fill), 0, -1):
            if level_fill[level] == 7:
                top_level = level
                break

        if top_level:
            remove = set(_ for _ in used_space if _.y < top_level)
            used_space -= remove

        # This code was part of what was used to find the magic numbers
        # (like cycle_height, cycle_length etc)
        # # Check for dropping a horizontal shape
        # if shape_index == 0:
        #     # If it is positioned like ".####.." print some data
        #     if Coord(0, max_y-4) not in used_space \
        #         and Coord(1, max_y-4) in used_space \
        #         and Coord(2, max_y-4) in used_space \
        #         and Coord(3, max_y-4) in used_space \
        #         and Coord(4, max_y-4) in used_space \
        #         and Coord(5, max_y-4) not in used_space \
        #         and Coord(6, max_y-4) not in used_space:
        #         d = max_y - lastround
        #         lastround = max_y
        #         # 127 was identified by looking at data being printed out.
        #         # Not my proudest moment.
        #         if d == 127:
        #             print(">>127", max_y-last_height_127, count)
        #             # 127 appears twice in the cycle, after 1953 and 621 iterations respectively.
        #             # This code helped identify that.
        #             if max_y - last_height_127 == 1953:
        #                 if seen:
        #                     increment = count - last_round_127
        #                     print(count, increment)
        #                     seen = False
        #                     # exit()
        #                 else:
        #                     seen = True
        #                     last_round_127 = count
        #             last_height_127 = max_y

    initial_height = max_y - FREELINES
    total_iterheight = ((MAX-(iterations_before_stabilization+final_rounds)) // cycle_length) * cycle_height
    return initial_height + total_iterheight


print("star1:", star1())
print("star2:", star2())
