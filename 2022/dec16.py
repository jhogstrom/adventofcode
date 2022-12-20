import os

runtest = False
stardate = 16
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Node():
    def __init__(self, line, maze) -> None:
        self.maze = maze
        self.name = line.split()[1]
        self._nodes = []
        self.flow = int(line.split()[4][5:-1])
        for _ in line.split()[::-1]:
            if "valve" in _:
                break
            n = _.strip(", ")
            self._nodes.append(n)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.name} ({self.flow}) -> {', '.join(self._nodes)}"

    def nodes(self):
        res = []
        for _ in self._nodes:
            res.append(self.maze[_])
        return res


def parse(data):
    maze = {}
    for _ in data:
        n = Node(_, maze)
        maze[n.name] = n
    return maze


def shortest_path(node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = last_node.nodes()
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if next_node not in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


def traverse_tree(
        *,
        maze,
        distances,
        start,
        time_left,
        visited=None,
        level=0,
        prohibited=None):
    if time_left <= 0:
        return 0
    if start not in distances:
        return 0
    visited = visited or [start]
    prohibited = prohibited or []
    res = []
    for n, cost in distances[start].items():
        if n.name not in visited and n.name not in prohibited:
            flowtime = time_left - cost - 1
            if flowtime <= 0:
                continue
            flow = flowtime * n.flow
            flow += traverse_tree(
                maze=maze,
                distances=distances,
                start=n.name,
                time_left=flowtime,
                visited=visited + [n.name],
                level=level+1,
                prohibited=prohibited)
            res.append(flow)
    res = res or [0]
    return max(res)


def all_distances(flownodes, start):
    dist = {}
    for _ in flownodes:
        p = shortest_path(start, _)
        if len(p) == 1:
            continue
        dist[p[-1]] = len(p) - 1
    return dist


def star1():
    maze = parse(data)
    flownodes = [_ for _ in maze.values() if _.flow]
    distances = {"AA": all_distances(flownodes, maze["AA"])}
    for _from in flownodes:
        distances[_from.name] = all_distances(flownodes, _from)

    return traverse_tree(
        maze=maze,
        distances=distances,
        start="AA",
        time_left=30)


def star2():
    maze = parse(data)
    flownodes = [_ for _ in maze.values() if _.flow]
    distances = {"AA": all_distances(flownodes, maze["AA"])}
    for _from in flownodes:
        distances[_from.name] = all_distances(flownodes, _from)

    nodenames = list(distances.keys())[1:]
    costs = list(distances.values())[1:]
    M = 0
    MAXTIME = 26
    for _ in range(2**(len(distances)-1)):
        mydist = {"AA": distances["AA"]}
        eldist = {"AA": distances["AA"]}
        my_flows = []
        el_flows = []
        b = bin(_)[2:].zfill(len(distances)-1)
        for i, d in enumerate(b):
            if d == "1":
                mydist[nodenames[i]] = costs[i]
                my_flows.append(nodenames[i])
            else:
                eldist[nodenames[i]] = costs[i]
                el_flows.append(nodenames[i])

        # Skip uneven distributions
        if abs(len(mydist) - len(eldist)) > 2:
            continue

        r = traverse_tree(
            maze=maze,
            distances=mydist,
            start="AA",
            time_left=MAXTIME,
            prohibited=el_flows)
        r += traverse_tree(
            maze=maze,
            distances=eldist,
            start="AA",
            time_left=MAXTIME,
            prohibited=my_flows)
        M = max(M, r)

    return M


print("star1:", star1())
print("star2:", star2())
