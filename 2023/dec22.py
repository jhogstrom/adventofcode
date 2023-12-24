from collections import defaultdict, deque
import logging
from reader import get_data, timeit, set_logging

runtest = False
stardate = "22"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)


class Block:
    def __init__(self, s, name=None, space=None) -> None:
        # print(s)
        ends = s.split("~")
        self.a = [int(_) for _ in ends[0].split(",")]
        self.b = [int(_) for _ in ends[1].split(",")]
        self.space = space
        if name:
            self.name = name

        for x in range(self.a[0], self.b[0] + 1):
            for y in range(self.a[1], self.b[1] + 1):
                for z in range(self.a[2], self.b[2] + 1):
                    space[(x, y, z)] = self

    def __repr__(self) -> str:
        if hasattr(self, "name"):
            return self.name
        return f"{self.a}~{self.b}"

    def canmove(self) -> bool:
        """
        First get the slice in the z direction
        Then check if any of the blocks in the slice can move.
        The block can move if the space below is empty for the entire slice.
        """
        x1, y1, z1 = self.a
        x2, y2, z2 = self.b
        if min([z1, z2]) == 1:
            return False
        for x in range(min([x1, x2]), max([x1, x2]) + 1):
            for y in range(min([y1, y2]), max([y1, y2]) + 1):
                if self.space.get((x, y, min([z1, z2]) - 1)):
                    return False
        # logging.debug(f"{self} can move")
        return True

    def move(self):
        """
        Move the block down one step.
        This means shifting the z coordinates one step down
        as well as updating the space dictionary.
        """
        # logging.debug(f"moving {self}")
        x1, y1, z1 = self.a
        x2, y2, z2 = self.b
        for x in range(min([x1, x2]), max([x1, x2]) + 1):
            for y in range(min([y1, y2]), max([y1, y2]) + 1):
                for z in range(min([z1, z2]), max([z1, z2]) + 1):
                    self.space[(x, y, z - 1)] = self
                    del self.space[(x, y, z)]
        self.a[2] -= 1
        self.b[2] -= 1

    def bricks_above(self) -> set:
        """
        Get the bricks above this block.
        """
        x1, y1, z1 = self.a
        x2, y2, z2 = self.b
        maxz = max([z1, z2])
        res = {
            self.space.get((x, y, maxz + 1))
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
        }
        return {_ for _ in res if _}

    def bricks_below(self) -> set:
        """
        Get the bricks below this block.
        """
        x1, y1, z1 = self.a
        x2, y2, z2 = self.b
        minz = min([z1, z2])
        res = {
            self.space.get((x, y, minz - 1))
            for x in range(min([x1, x2]), max([x1, x2]) + 1)
            for y in range(min([y1, y2]), max([y1, y2]) + 1)
        }
        return {_ for _ in res if _}# and _ != self}


def print_space(space, show):
    miny = min([y for _, y, _ in space.keys()])
    maxy = max([y for _, y, _ in space.keys()])
    minx = min([x for x, _, _ in space.keys()])
    maxx = max([x for x, _, _ in space.keys()])
    minz = min([z for _, _, z in space.keys()])
    maxz = max([z for _, _, z in space.keys()])

    for z in range(maxz, minz-1, -1):
        print(f"{z:3} ", end="")
        for x in range(minx, maxx + 1):
            s = set()
            for y in range(miny, maxy + 1):
                b = space.get((x, y, z))
                if b:
                    s.add(b.name)
            if len(s) == 0:
                print(".", end="")
            elif len(s) == 1:
                print(list(s)[0], end="")
            else:
                print("?", end="")
        print()
    print("===")


def parse_data(data):
    space = {}
    blocks = []
    name = "A"
    for _ in data:
        blocks.append(Block(_, name=name, space=space))
        name = chr(ord(name) + 1)
    logging.debug(f"Total blocks: {len(blocks)}")
    return blocks


def pack_blocks(space):
    miny = min([y for _, y, _ in space.keys()])
    maxy = max([y for _, y, _ in space.keys()])
    minx = min([x for x, _, _ in space.keys()])
    maxx = max([x for x, _, _ in space.keys()])
    minz = min([z for _, _, z in space.keys()])
    maxz = max([z for _, _, z in space.keys()])
    for z in range(minz, maxz + 1):
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                block = space.get((x, y, z))
                if block:
                    while block.canmove():
                        block.move()


@timeit
def star1(data):
    logging.debug("running star 1")
    blocks = parse_data(data)
    # print_space(space, "x")

    # Packing blocks
    pack_blocks(blocks[0].space)
    # print_space(space, "x")

    res = len([b for b in blocks if all([len(above.bricks_below()) > 1 for above in b.bricks_above()])])
    # for b in blocks:
    #     bricks_above = b.bricks_above()
    #     logging.debug(f"Examining {b} - supporting {bricks_above}")
    #     can_disintegrate = all([len(above.bricks_below()) > 1 for above in bricks_above])
    #     for above in bricks_above:
    #         logging.debug(f"\t{above} rests on {above.bricks_below()}")

    #     if can_disintegrate:
    #         res += 1
    #         logging.debug(f"=> {b} can be removed")
    #     else:
    #         logging.debug(f"=> {b} cannot be removed")
    print(res)


@timeit
def star2(data):
    logging.debug("running star 2")
    blocks = parse_data(data)
    # print_space(space, "x")

    # Packing blocks
    pack_blocks(blocks[0].space)
    # print_space(space, "x")

    res = 0
    for b in [_ for _ in blocks if not all([len(above.bricks_below()) > 1 for above in _.bricks_above()])]:
        fallen, q = {b}, deque([b])
        while q:
            n = q.pop()
            for a in n.bricks_above():
                if a in fallen:
                    continue
                if all([_ in fallen for _ in a.bricks_below()]):
                    # logging.debug(f"All of the bricks below {a} ({a.bricks_below()}) have fallen.")
                    q.append(a)
                    fallen.add(a)
        # logging.debug(f"Fallen: {fallen - {b}} - {len(fallen)-1}")
        res += len(fallen) - 1
    print(res)


star1(data)
star2(data)
