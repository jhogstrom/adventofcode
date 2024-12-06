import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "06"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def find(char, data):
    for i, line in enumerate(data):
        if char in line:
            return (i, line.index(char))


def within_board(data, pos):
    return 0 <= pos[0] < len(data) and 0 <= pos[1] < len(data[0])


def next_pos(pos, move):
    return (pos[0] + move[0], pos[1] + move[1])


@timeit
def star1(data, printit: bool = True):
    if printit:
        logging.debug("running star 1")
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction = 0

    pos = find("^", data)
    visited = [(pos, direction)]
    while within_board(data, next_pos(pos, directions[direction])):
        n = next_pos(pos, directions[direction])
        if data[n[0]][n[1]] == "#":
            direction = (direction + 1) % 4
        else:
            pos = n
            visited.append((pos, direction))

    result = {p for p, _ in visited}
    if printit:
        print(len(result))
    return visited


def escape(data, pos, direction):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited = {(pos, direction)}
    while within_board(data, next_pos(pos, directions[direction])):
        n = next_pos(pos, directions[direction])
        if data[n[0]][n[1]] in "#O":
            direction = (direction + 1) % 4
            continue
        pos = n
        if (pos, direction) in visited:
            # print("LOOP")
            # print_grid(data, pos, visited)
            return False
        visited.add((pos, direction))
    return True


def print_grid(data, pos, path, count: int = None):
    # path_markers = "|-|-"
    for y, s in enumerate(data):
        for x, c in enumerate(s):
            if (y, x) == pos:
                print("X", end="")
            elif (y, x) in {p for p, _ in path}:
                print("+", end="")
            else:
                print(c, end="")
        print()
    print()
    if count is not None:
        print(f"^^^^^ {count} ^^^^^")
    input()


@timeit
def star2(data):
    logging.debug("running star 2")
    path = star1(data, False)
    blocks = set()

    for i in range(len(path) - 1):
        field = data[:]
        next = path[i + 1][0]
        field[next[0]] = (
            field[next[0]][: next[1]] + "O" + field[next[0]][next[1] + 1 :]  # noqa E203
        )
        if not escape(field, path[0][0], path[0][1]):
            if next not in blocks:
                blocks.add(next)
                # print_grid(field, move[0][0], path[: i + 1], len(blocks))

    print(len(blocks))


star1(data)
star2(data2)
