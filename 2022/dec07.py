import os

runtest = False
stardate = "07"
if runtest:
    dataname = f"dec{stardate}test.txt"
    print("USING TESTDATA")
else:
    dataname = f"dec{stardate}.txt"

curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Node:
    def __init__(self, name, parent) -> None:
        self.name = name
        self._size = 0
        self.parent = parent

    def __str__(self) -> str:
        return self.fullname()

    def size(self):
        return self._size

    def fullname(self):
        if self.parent is None:
            return "$"
        return self.parent.fullname() + "/" + self.name


class Directory(Node):
    def __init__(self, name, parent) -> None:
        super().__init__(name, parent)
        self.children = []

    def size(self):
        return sum([_.size() for _ in self.children])


class File(Node):
    def __init__(self, name, parent, size) -> None:
        super().__init__(name, parent)
        self._size = size


def parse_data():
    root = Directory("$", None)
    cwd = root
    for _ in data[1:]:
        # print(_)
        parts = _.split()
        if parts[0] == "$" and parts[1] == "ls":
            continue
        if parts[0] == "$" and parts[1] == "cd":
            if parts[2] == "..":
                # print(">>>", cwd.fullname(), cwd.size())
                cwd = cwd.parent
                continue
            for c in cwd.children:
                if c.name == parts[2]:
                    cwd = c
            continue
        if parts[0] == "dir":
            cwd.children.append(Directory(parts[1], cwd))
        else:
            cwd.children.append(File(parts[1], cwd, int(parts[0])))
    return root


totalsize = 0


def get_sizes(d, level: int = 0):
    global totalsize
    size = d.size()
    # print("-" * level, d.fullname(), size)
    if size <= 100000:
        totalsize = size
    else:
        totalsize = 0
    for c in d.children:
        if isinstance(c, Directory):
            totalsize += get_sizes(c, level+1)
    return totalsize


def star1():
    root = parse_data()

    return get_sizes(root)


def find_smallest_to_delete(d, smallest, free_space, level: int = 0):
    REQ_SPACE = 30_000_000
    size = d.size()
    # print("-" * level, d.fullname(), size)
    if size + free_space > REQ_SPACE:
        smallest = min([smallest, size])
    for c in d.children:
        if isinstance(c, Directory):
            smallest = min([smallest, find_smallest_to_delete(c, smallest, free_space, level+1)])
    return smallest


def star2():
    TOTAL_SPACE = 70_000_000
    root = parse_data()

    FREE_SPACE = TOTAL_SPACE - root.size()
    smallest = find_smallest_to_delete(root, root.size(), FREE_SPACE)
    return smallest


print("star1:", star1())
print("star2:", star2())


# Equivalent solution, slightly less code
def flatten(node):
    result = [node.size()]
    for _ in [d for d in node.children if isinstance(d, Directory)]:
        result.extend(flatten(_))
    return result


sizes = flatten(parse_data())
free_space = 70_000_000 - sizes[0]
print("star1:", sum([_ for _ in sizes if _ < 100_000]))
print("star2:", min([_ for _ in sizes if _ + free_space > 30_000_000]))
