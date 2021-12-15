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
        if not self.parent:
            self._cost = self.value
            return self.value
        res = self.value + self.parent.cost
        self._cost = res
        return res

    def __str__(self) -> str:
        return f"{self.pos} - {self.value}"


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


def findpath(maze, start, end):
    # Create start and end node
    start_node = Node(None, start, maze[start[1]][start[0]])
    start_node.g = start_node.value
    end_node = Node(None, end, maze[end[1]][end[0]])

    # Initialize both open and closed list
    candidates = []
    visited = []

    # Add the start node
    candidates.append(start_node)

    # Loop until you find the end
    while len(candidates) > 0:

        best_node = candidates[0]
        for _ in candidates:
            if _.cost < best_node.cost:
                best_node = _

        current = best_node
        candidates.remove(best_node)
        visited.append(current)
        # print(f"Looking at {current}")
        if current == end_node:
            path = []
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1] # Return reversed path

        for child in [_ for _ in get_neighbors(maze, current) if _ not in visited]:
            if child in visited:
                vnode = [_ for _ in visited if _ == child]
                if vnode.cost > child.cost:
                    vnode.set_parent(current)
            if child not in candidates:
                candidates.append(child)


@timeit
def star1(data):
    maze = []
    for s in data:
        maze.append([int(_) for _ in s])
    # print(maze)

    path = findpath(maze, (0, 0), (len(maze[0])-1, len(maze)-1))

    # for _ in path:
    #     print(_)
    # print([str(_) for _ in path])
    print(sum(_.value for _ in path[1:]))


@timeit
def star2(data):
    ...

data2 = data[:]
star1(data)
star2(data2)