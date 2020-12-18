import os
from timing import timeit

filename = os.path.abspath(__file__).replace(".py", ".txt")
if not os.path.exists(filename):
    raise Exception(f"'{filename} does not exist")
data = [_.strip() for _ in open(filename, 'r').readlines()]


def tokenize(s):
    expr = s.split()
    tokens = []
    for t in expr:
        # print(t)
        while t[0] == "(":
            tokens.append("(")
            t = t[1:]


        _tokens = []
        while t[-1] == ")":
            _tokens.append(")")
            t = t[:-1]

        if t.isnumeric():
            t = int(t)

        tokens.append(t)
        if _tokens:
            tokens += _tokens
    return tokens


def make_tree(tokens, level=0):
    # print(f"{'-' * level} tokens: {tokens}")
    stack = []
    n = 0
    while n < len(tokens):
        if tokens[n] == "(":
            pcount = 1
            c = n+1
            while pcount > 0:
                if tokens[c] == "(":
                    pcount += 1
                elif tokens[c] == ")":
                    pcount -= 1
                c += 1
            subexpr = tokens[n+1:c-1]
            # print(f"{'-' * level} subexpr: {subexpr}")
            stack.append(make_tree(subexpr, level+1))

            tokens = tokens[:n] + [make_tree(subexpr, level+1)] + tokens[c:]
            # print(f"{'-' * level} remaining: {tokens}")
        else:
            # print(f"{'-' * level} appending: {tokens[n]}")
            stack.append(tokens[n])
        n += 1

    # print(f"{'-' * level} So far: {stack}")
    return stack


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


ops = {
    '+': add,
    '*': mul
}


def evaluate_tree(tree):
    # print(f"Evaluating: {tree}")
    if isinstance(tree, int):
        return tree
    while len(tree) > 1:
        res = ops[tree[1]](evaluate_tree(tree[0]), evaluate_tree(tree[2]))
        tree = [res] + tree[3:]
        # print(f"New tree = {tree}")
    return res


def evaluate_tree2(tree):
    # print(f"Evaluating: {tree}")
    if isinstance(tree, int):
        return tree
    while '+' in tree:
        p = tree.index('+')
        res = ops[tree[p]](evaluate_tree2(tree[p-1]), evaluate_tree2(tree[p+1]))
        tree = tree[:p-1] + [res] + tree[p+2:]
        # print(f"New tree (+) = {tree}")
    while len(tree) > 1:
        res = ops[tree[1]](evaluate_tree2(tree[0]), evaluate_tree2(tree[2]))
        tree = [res] + tree[3:]
    # print(f"New tree (+) = {tree}")
    return res


# data = ["1 + 2 * 3 + 4 * 5 + 6",
# "2 * 3 + (4 * 5)",
# "5 + (8 * 3 + 9 + 3 * 4 * 3)",
# "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
# "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
# ]


def star1():
    res = 0
    for expr in data:
        tokens = tokenize(expr)
        tree = make_tree(tokens)
        res += evaluate_tree(tree)
    return res


def star2():
    res = 0
    for expr in data:
        tokens = tokenize(expr)
        tree = make_tree(tokens)
        res += evaluate_tree2(tree)
    return res

print(f"* {star1()}")
print(f"** {star2()}")
