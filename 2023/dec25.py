import logging
from collections import defaultdict
from pprint import pprint
from random import randint

from reader import get_data, set_logging, timeit

runtest = True
stardate = "25"
year = "2023"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


@timeit
def star1(data):
    logging.debug("running star 1")
    # print("digraph G {")
    # for d in data:
    #     p = d.split(" ")
    #     s = p[0][:3] + " -> " + ",".join(p[1:]) + ";"
    #     print(s)
    # print("}")

    graph = defaultdict(set)
    for d in data:
        p = d.split(" ")
        p[0] = p[0][:3]
        for n in p[1:]:
            graph[n].add(p[0])
            graph[p[0]].add(n)

    pprint(graph)
    nodecounter = {_: 1 for _ in graph}
    print(nodecounter)

    while len(graph) > 2:
        i = randint(0, len(graph) - 1)
        n1 = list(graph.keys())[i]
        ends = graph[n1]
        del graph[n1]
        print(f"{n1} -> {ends} -- ", end="")
        n2 = ends.pop()
        print(f"{n2} -> {graph[n2]}")
        graph[n2].remove(n1)
        graph[n2].update(ends)
        for k, v in graph.items():
            if n1 in v and k != n2:
                v.remove(n1)
                v.add(n2)
        print(f"Removing {n2} -> {n1}. Updating {n2} -> {graph[n2]}")
        nodecounter[n2] += nodecounter[n1]
        del nodecounter[n1]
        pprint(graph)
        print(nodecounter)
        # input()


@timeit
def star2(data):
    logging.debug("running star 2")


star1(data)
star2(data2)
