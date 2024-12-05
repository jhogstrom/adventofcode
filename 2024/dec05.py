import logging
from collections import defaultdict
from typing import Dict, List

from reader import get_data, set_logging, timeit

runtest = False
stardate = "05"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


def correctly_ordered(pageset: List[int], rules: Dict[int, List[int]]):
    for i, p in enumerate(pageset):
        for p_before, p_after in rules.items():
            if p_before == p:
                for a in p_after:
                    if a in pageset and a not in pageset[i + 1 :]:  # noqa E203
                        return False

    return True


def get_rules(data: List[str]) -> Dict[int, List[int]]:
    rules = defaultdict(set)
    for s in data:
        if not s:
            break
        rules[int(s.split("|")[0])].add(int(s.split("|")[1]))
    return rules


def get_pagesets(data: List[str]) -> List[List[int]]:
    pagesets = []
    rule_section = True
    for s in data:
        if not s:
            rule_section = False
            continue
        if rule_section:
            continue
        pagesets.append([int(x) for x in s.split(",")])
    return pagesets


@timeit
def star1(data):
    logging.debug("running star 1")
    rules = get_rules(data)
    pagesets = get_pagesets(data)
    result = 0
    for pageset in pagesets:
        if correctly_ordered(pageset, rules):
            middle_page = pageset[len(pageset) // 2]
            result += middle_page
    print(result)


def reorder(pageset: List[int], rules: Dict[int, List[int]]):
    while not correctly_ordered(pageset, rules):
        for i, p in enumerate(pageset):
            for p_before, p_after in rules.items():
                if p_before == p:
                    for a in p_after:
                        if a in pageset and a not in pageset[i + 1 :]:  # noqa E203
                            pageset.remove(a)
                            pageset.insert(i, a)
    return pageset


@timeit
def star2(data):
    logging.debug("running star 2")
    rules = get_rules(data)
    pagesets = get_pagesets(data)
    result = 0
    for pageset in pagesets:
        if not correctly_ordered(pageset, rules):
            pageset = reorder(pageset, rules)
            middle_page = pageset[len(pageset) // 2]
            result += middle_page
    print(result)


star1(data)
star2(data2)
