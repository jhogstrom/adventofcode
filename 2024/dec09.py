import logging
from typing import List

from reader import get_data, set_logging, timeit

runtest = False
stardate = "09"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def printout(sectors: List[int]) -> None:
    sector_representation = []
    for sector in sectors:
        if sector == -1:
            sector_representation.append(".")
        else:
            sector_representation.append(str(sector))
    print("".join(sector_representation))


@timeit
def star1(data):
    logging.debug("running star 1")
    sectors = get_sectors(data)

    i = 0
    tail = len(sectors)
    while i < tail:
        if sectors[i] == -1:
            f = -1
            while f == -1:
                tail -= 1
                f = sectors[tail]
            sectors[i] = f
            sectors[tail] = -1
        i += 1
        # printout(sectors)

    res = 0
    for p, c in enumerate(sectors[:tail]):
        res += p * c

    print(res)


class Block:
    def __init__(self, size, filenum):
        self.size = size
        self.filenum = filenum

    def is_empty(self) -> bool:
        return self.filenum == -1

    def copy(self) -> "Block":
        return Block(self.size, self.filenum)

    def __repr__(self):
        return f"Block({self.size=}, {self.filenum=})"


def print_blocks(blocks: List[Block]) -> None:
    repr = []
    for b in blocks:
        for _ in range(b.size):
            if b.filenum == -1:
                repr.append(".")
            else:
                repr.append(str(b.filenum))
    print("".join(repr))


def get_sectors(data: str) -> List[int]:
    sectors = []
    filenum = -1
    for i, c in enumerate(data):
        if i % 2 == 0:
            filenum += 1
        for _ in range(int(c)):
            sectors.append(filenum if i % 2 == 0 else -1)
    # printout(sectors)
    return sectors


def make_blocks(sectors: List[int]) -> List[Block]:
    blocks = []
    for s in sectors:
        if not blocks or blocks[-1].filenum != s:
            blocks.append(Block(1, s))
        else:
            blocks[-1].size += 1
    # print_blocks(blocks)
    return blocks


@timeit
def star2(data):
    logging.debug("running star 2")
    sectors = get_sectors(data)
    blocks = make_blocks(sectors)

    block_to_move = len(blocks) - 1
    while block_to_move > 0:
        while blocks[block_to_move].is_empty():
            block_to_move -= 1

        first_fitting_block = 0
        while not (
            blocks[first_fitting_block].is_empty()
            and blocks[first_fitting_block].size >= blocks[block_to_move].size
        ):
            first_fitting_block += 1
            if first_fitting_block >= block_to_move:
                block_to_move -= 1
                break

        if first_fitting_block >= block_to_move:
            continue

        blocks[first_fitting_block].filenum = blocks[block_to_move].filenum
        blocks[block_to_move].filenum = -1
        if blocks[first_fitting_block].size > blocks[block_to_move].size:
            new_block = Block(
                blocks[first_fitting_block].size - blocks[block_to_move].size, -1
            )
            blocks[first_fitting_block].size = blocks[block_to_move].size
            blocks.insert(first_fitting_block + 1, new_block)
        # print_blocks(blocks)

    p = 0
    res = 0
    for b in blocks:
        if b.is_empty():
            p += b.size
        else:
            for _ in range(b.size):
                res += p * b.filenum
                p += 1
    print(res)


star1(data[0])
star2(data2[0])
