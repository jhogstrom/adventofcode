import os
from timer import timeit
from collections import defaultdict


stardate = 20
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


map_to_binary_digit = { True: "1", False: "0"}


def print_image(image):
    yrange = set(_[1] for _ in image)
    xrange = set(_[0] for _ in image)

    for y in range(min(yrange), max(yrange)+1):
        print(f"{y:>3} ", end="")
        for x in range(min(xrange), max(xrange)+1):
            print("#" if image[(x, y)] else ".", end="")
        print()
    print("==")


def constant_factory(value):
    return lambda: value


def apply_filter(image: defaultdict, filter) -> defaultdict:
    yrange = [_[1] for _ in image]
    xrange = [_[0] for _ in image]
    x_scan_range = range(min(xrange)-1, max(xrange)+2)
    y_scan_range = range(min(yrange)-1, max(yrange)+2)

    ix = 511 if image.default_factory() else 0
    res = defaultdict(constant_factory(filter[ix]))

    for y in y_scan_range:
        ypixrange = range(y-1, y+2)
        for x in x_scan_range:
            xpixrange = range(x-1, x+2)
            index = []
            for yi in ypixrange:
                for xi in xpixrange:
                    index.append(map_to_binary_digit[image[(xi, yi)]])
            res[(x, y)] = filter[int("".join(index), 2)]
    return res


def count_pixels(image):
    return sum(1 for _ in image.values() if _)


@timeit
def evolve_image(data, gen_count):
    filter = [_ == "#" for _ in data[0]]
    assert(len(filter) == 512)
    image = defaultdict(constant_factory(not filter[0]))

    for y, s in enumerate(data[2:]):
        for x, c in enumerate(s):
            image[(x, y)] = c == "#"

    for _ in range(gen_count):
        image = apply_filter(image, filter)
    # print_image(image)
    print(count_pixels(image))


evolve_image(data, 2)
evolve_image(data, 50)