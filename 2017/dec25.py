from collections import defaultdict

rules = \
{
    'A': [[1, 1, 'B'], [0,-1,'C']],\
    'B': [[1,-1,'A'], [1,1,'C']], \
    'C': [[1,1,'A'], [0,-1,'D']], \
    'D': [[1,-1,'E'], [1,-1,'C']], \
    'E': [[1,1,'F'], [1,1,'A']], \
    'F': [[1,1,'A'], [1,1,'E']], \
  }

for k in rules:
    print(k)
    print(rules[k][0])
    print(rules[k][1])

pos = 0
state = 'A'
tape = defaultdict(int)

steps = 12134527
#steps = 10
for i in range(steps):
    w, m, s = rules[state][tape[pos]]
    tape[pos] = w
    pos += m
    state = s
    if i % 10000 == 0:
        print(i)

print(sum(tape.values()))