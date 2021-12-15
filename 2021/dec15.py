import os
from timer import timeit
from collections import defaultdict, deque

stardate = 15
dataname = f"dec{stardate}.txt"
# dataname = f"dec{stardate}_test.txt"
curdir = os.path.dirname(os.path.abspath(__file__))
filename = f'{curdir}\\{dataname}'
data = [_.strip() for _ in open(filename, 'r').readlines()]
if not data:
    raise FileNotFoundError(f"No data in {dataname}")


class Node():
    def __init__(self, parent, pos, value) -> None:
        self.pos = pos
        self.parent = parent
        self.value = value
        self.f = self.g = self.h = 0
        self._cost = -1

    def __eq__(self, __o: object) -> bool:
        return self.pos[0] == __o.pos[0] and self.pos[1] == __o.pos[1]

    def set_parent(self, parent):
        self.parent = parent
        self._cost = -1

    @property
    def cost(self):
        if self._cost > -1:
            return self._cost
        if not self.parent:  # Start node doesn't count
            self._cost = 0
            return 0
        res = self.value + self.parent.cost
        self._cost = res
        return res

    def __str__(self) -> str:
        return f"{self.pos} - {self.value} ({self.cost})"


def get_neighbors(maze, current):
    res = []
    for neighbor_pos in [
                     (-1, 0),
            (0, -1),            (0, 1),
                     (1, 0),            ]:

        # Get node position
        nexty = current.pos[1] + neighbor_pos[1]
        nextx = current.pos[0] + neighbor_pos[0]
        if nextx < 0 or nexty < 0 or nextx == len(maze) or nexty == len(maze):
            continue
        res.append(Node(current, (nextx, nexty), maze[nexty][nextx]))
    return res


def dijkstra(maze, start, end):
    # Create start and end node
    start_node = Node(None, start, maze[start[1]][start[0]])
    start_node.g = start_node.value
    end_node = Node(None, end, maze[end[1]][end[0]])

    # Initialize both open and closed list
    candidates = []
    visited = []

    # Add the start node
    candidates.append(start_node)
    c = 0

    # Loop until you find the end
    while len(candidates) > 0:
        c += 1

        current = candidates[0]
        for _ in candidates[1:]:
            if _.cost < current.cost:
                current = _

        if c % 1000 == 0:
            print(f"Count: {c:<7} {current} Visited: {len(visited)} Candidates: {len(candidates)}")
        candidates.remove(current)
        visited.append(current)
        # print(f"Looking at {current}")
        if current == end_node:
            path = []
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1] # Return reversed path

        for child in [_ for _ in get_neighbors(maze, current) if _ not in visited]:
            # if child in visited:
            #     vnode = [_ for _ in visited if _ == child]
            #     if vnode.cost > child.cost:
            #         print(f"Replacing {vnode} with {child}")
            #         vnode.set_parent(current)
            if child not in candidates:
                candidates.append(child)


@timeit
def star1(data):
    maze = []
    for s in data:
        maze.append([int(_) for _ in s])


    path = dijkstra(maze, (0, 0), (len(maze[0])-1, len(maze)-1))

    # for _ in path:
    #     print(_)

    print(path[-1].cost)


@timeit
def star2(data):
    maze = []
    for i in range(5):
        for s in data:
            row = []
            for j in range(5):
                row.extend([int(_)+j+i for _ in s])
            for f in range(len(row)):
                row[f] = row[f] % 9 or 9
            maze.append(row)

    for _ in maze:
        print(_)
    # exit()
    path = dijkstra(maze, (0, 0), (len(maze[0])-1, len(maze)-1))

    for _ in path:
        print(_)

    print(path[-1].cost)

# data2 = data[:]
# star1(data)
star2(data)