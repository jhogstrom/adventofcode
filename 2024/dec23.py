import itertools
import logging
from collections import defaultdict

from reader import get_data, set_logging, timeit

runtest = False
stardate = "23"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    groups = [set(_.split("-")) for _ in data]
    i = 0
    result = []
    while i < len(groups):
        j = i + 1
        while j < len(groups):
            if any(_ in groups[i] for _ in groups[j]):
                group = groups[i].union(groups[j])
                if any(_.startswith("t") for _ in group):
                    k = j + 1
                    while k < len(groups):
                        if all(_ in group for _ in groups[k]):
                            s = ", ".join(sorted(group))
                            result.append(s)
                        k += 1
            j += 1
        i += 1
        print(i, end="\r")

    print(len(result))


def bron_kerbosch(graph, r=set(), p=None, x=set()):
    if p is None:
        p = set(graph.keys())

    if not p and not x:
        yield r
    else:
        u = next(iter(p | x))  # Choose a pivot vertex
        for v in p - graph[u]:
            yield from bron_kerbosch(graph, r | {v}, p & graph[v], x & graph[v])
            p.remove(v)
            x.add(v)


def find_largest_complete_subgraph(graph):
    cliques = list(bron_kerbosch(graph))
    return max(cliques, key=len)


@timeit
def star2(data):
    logging.debug("running star 2")
    groups = [_.split("-") for _ in data]
    connections = defaultdict(set)
    for g in groups:
        connections[g[0]].add(g[1])
        connections[g[1]].add(g[0])
    res = find_largest_complete_subgraph(connections)
    print(",".join(sorted(res)))


@timeit
def star1_bk(data):
    logging.debug("running star 1")
    groups = [_.split("-") for _ in data]
    connections = defaultdict(set)
    for g in groups:
        connections[g[0]].add(g[1])
        connections[g[1]].add(g[0])
    clicques = list(bron_kerbosch(connections))

    eligeble = set()
    for c in (_ for _ in clicques if len(_) >= 3 and any(n.startswith("t") for n in _)):
        for i in itertools.combinations(c, 3):
            if any(_.startswith("t") for _ in i):
                eligeble.add(tuple(sorted(i)))
    print(len(eligeble))


# star1(data)
star1_bk(data)
star2(data2)
