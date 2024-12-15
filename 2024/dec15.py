import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "15"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def parse_data(data):
    room = []
    for _ in data:
        if not _:
            break
        room.append(list(_))
    moves = data[len(room) + 1 :]  # noqa E203
    moves = "".join(moves)
    return room, moves


def find_pos(room):
    for y, line in enumerate(room):
        for x, c in enumerate(line):
            if c == "@":
                return x, y


def calc_values(room, target):
    result = 0
    for y, line in enumerate(room):
        for x, c in enumerate(line):
            if c == target:
                result += 100 * y + x
    return result


def can_move(room, pos, move):
    x, y = pos
    while room[y][x] != "#":
        x += move[0]
        y += move[1]
        if room[y][x] == ".":
            return True

    return False


def make_move(room, pos, move):
    # print(f"Moving {move} from {pos}")
    x, y = pos
    xd, yd = move
    xsteps = xd
    ysteps = yd
    while room[y + ysteps][x + xsteps] in "O":
        xsteps += xd
        ysteps += yd

    xx, yy = 0, 0
    while any([xsteps + xd, ysteps + yd]):
        if room[y + yy][x + xx] == "#":
            break
        room[y + yy][x + xx] = "O"
        xx += xd
        yy += yd
        xsteps -= xd
        ysteps -= yd

    x, y = pos
    room[y][x] = "."
    room[y + yd][x + xd] = "@"

    return x + xd, y + yd


def print_room(room, wait: bool = True):
    for y, line in enumerate(room):
        print("".join(line))
    print()
    if wait:
        input()


def make_moves(room, pos, moves):
    move_dir = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
    for m in moves:
        if not can_move(room, pos, move_dir[m]):
            continue
        pos = make_move(room, pos, move_dir[m])
        # print_room(room)


@timeit
def star1(data):
    logging.debug("running star 1")
    room, moves = parse_data(data)
    pos = find_pos(room)
    make_moves(room, pos, moves)
    result = calc_values(room, "O")
    print(result)


def expand_space(room):
    for i in range(len(room)):
        line = room[i]
        result = []
        for c in line:
            if c == "#":
                result.append("##")
            elif c == "O":
                result.append("[]")
            elif c == ".":
                result.append("..")
            elif c == "@":
                result.append("@.")
            else:
                raise ValueError(f"Unknown character {c}")
        result = list("".join(result))
        room[i] = result
    return room


def get_next_row(room, row, move):
    # print("Getting next row from ", row)
    result = set()
    for x, y in row:
        next_char = room[y + move][x]
        if next_char in "[]":
            result.add((x, y + move))
            if next_char == "[":
                result.add((x + 1, y + move))
            elif next_char == "]":
                result.add((x - 1, y + move))
    return result


def peek_next_row(room, row, move):
    result = set()
    for x, y in row:
        if room[y][x] == ".":
            continue
        next_char = room[y + move][x]

        result.add((x, y + move))
        if next_char == "[":
            result.add((x + 1, y + move))
        elif next_char == "]":
            result.add((x - 1, y + move))
    return result


def can_move2(room, pos, move):
    x, y = pos
    dx, dy = move
    if dx:
        while room[y][x] != "#":
            x += dx
            if room[y][x] == ".":
                return True
        return False

    next_row = [(x, y)]
    while True:
        next_row = peek_next_row(room, next_row, dy)
        if all([room[y][x] == "." for x, y in next_row]):
            return True
        if any([room[y][x] == "#" for x, y in next_row]):
            return False


def make_move2(room, pos, move):
    x, y = pos
    dx, dy = move
    if move in ((-1, 0), (1, 0)):
        xsteps = 0
        while room[y][x + xsteps] in "[]@":
            xsteps += move[0]
        while xsteps:
            room[y][x + xsteps] = room[y][x + xsteps - dx]
            xsteps -= dx
        room[y][x + dx] = "@"
    else:
        blocks = [[(x, y)]]
        while not all(
            [room[y][x] == "." for x, y in get_next_row(room, blocks[-1], dy)]
        ):
            blocks.append(get_next_row(room, blocks[-1], dy))

        blocks = blocks[::-1]
        for block in blocks:
            for x, y in block:
                room[y + dy][x] = room[y][x]

        for i, block in enumerate(blocks[:-1]):
            for x, y in block:
                if (x, y - dy) not in blocks[i + 1]:
                    room[y][x] = "."
    x, y = pos
    room[y][x] = "."

    return (pos[0] + move[0], pos[1] + move[1])


def make_moves2(room, pos, moves):
    move_dir = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
    for i, m in enumerate(moves):
        # print(f"Move {i+1} {m} (next: {moves[i+1:i+4]})")
        if not can_move2(room, pos, move_dir[m]):
            # print("** Cannot move **\n")
            continue
        pos = make_move2(room, pos, move_dir[m])
        # print_room(room, wait=False)


@timeit
def star2(data):
    logging.debug("running star 2")
    room, moves = parse_data(data)
    room = expand_space(room)
    pos = find_pos(room)
    # print_room(room)
    make_moves2(room, pos, moves)
    result = calc_values(room, "[")
    print(result)


star1(data)
star2(data2)
