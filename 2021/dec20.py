import os
from timer import timeit
from collections import defaultdict, deque

stardate = 20
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


def print_image(image):
    yrange = set(_[1] for _ in image)
    xrange = set(_[0] for _ in image)

    for y in range(min(yrange), max(yrange)+1):
        print(f"{y:>3} ", end="")
        for x in range(min(xrange), max(xrange)+1):
            print("#" if image[(x, y)] else ".", end="")
        print()
    print("==")


def apply_filter(image: defaultdict, filter):
    yrange = set(_[1] for _ in image)
    xrange = set(_[0] for _ in image)

    ix = 511 if image.default_factory() else 0
    res = defaultdict(constant_factory(filter[ix] == "#"))

    for y in range(min(yrange)-1, max(yrange)+2):
        for x in range(min(xrange)-1, max(xrange)+2):
            index = []
            for yi in range(y-1, y+2):
                for xi in range(x-1, x+2):
                    index.append("1" if image[(xi, yi)] else "0")
            indexb = "".join(index)
            index = int(indexb, 2)
            # print(f"({x:>2}, {y:>2}): {index:>3}  -> {'#' if image[(x, y)] else '.'}->{filter[index]} [{indexb}]")
            res[(x, y)] = filter[index] == "#"

    # yrange = set(_[1] for _ in res)
    # xrange = set(_[0] for _ in res)
    # print(f"BB: ({min(xrange)}, {min(yrange)}) -> ({max(xrange)}, {max(yrange)})")

    return res


def count_pixels(image):
    return len([_ for _ in image.values() if _])


def constant_factory(value):
    return lambda: value


@timeit
def evolve_image(data, gen_count):
    filter = data[0]
    assert(len(filter) == 512)
    image = defaultdict(constant_factory(filter[0] == "."))

    for i, s in enumerate(data[2:]):
        for j, c in enumerate(s):
            image[(j, i)] = c == "#"

    # print_image(image)
    # print(count_pixels(image))

    for i in range(gen_count):
        image = apply_filter(image, filter)
        # print_image(image)
        # print(i+1, count_pixels(image))
    # print_image(image)
    print(count_pixels(image))


evolve_image(data, 2)
evolve_image(data, 50)