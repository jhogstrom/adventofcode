inp = open('12.txt').readlines()
pipes = dict()

for l in inp:
    p = l.replace(",","").split()
    pipes[p[0]] = p[2:]

groups = dict()

def spantree(root, node):
    if not root in groups:
        groups[root] = []
    for c in node:
        if not c in groups[root]:
            groups[root].append(c)
            spantree(root,pipes[c])

def connected(n):
    for g in groups.values():
        if n in g:
            return True
    return False

for p in pipes:
    if not connected(p):
        spantree(p, pipes[p])

print(len(groups['0']), groups['0'])
print(len(groups))