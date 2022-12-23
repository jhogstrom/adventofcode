import os

runtest = False
stardate = 21
if runtest:
    print("USING TESTDATA")
dataname = f"dec{stardate}{'test' if runtest else ''}.txt"

filename = f'{os.path.dirname(os.path.abspath(__file__))}\\{dataname}'
data = open(filename, "r").read().splitlines()


class Monkey():
    def __init__(self, line) -> None:
        parts = line.split(":")
        self.name = parts[0]
        if parts[1].strip().isnumeric():
            self._value = int(parts[1])
            self.resolved = True
            return

        self.resolved = False
        calc = parts[1].split()
        self.lvalue = calc[0]
        self.op = calc[1]
        self.rvalue = calc[2]

    def calc(self, t1: int, t2: int) -> int:
        if self.op == "+":
            return t1 + t2
        elif self.op == "-":
            return t1 - t2
        elif self.op == "*":
            return t1 * t2
        elif self.op == "/":
            return t1 // t2
        elif self.op == "==":
            return t1 == t2
        raise ValueError("No such operator:", self.op)

    def solve(self):
        if self.resolved:
            return self._value

        return self.calc(self.lvalue.solve(), self.rvalue.solve())

    def get_tree(self):
        if self.resolved:
            return str(self._value)

        if self.lvalue.resolved:
            t1 = self.lvalue._value
        else:
            t1 = f"({self.lvalue.get_tree()})"
        if self.rvalue.resolved:
            t2 = self.rvalue._value
        else:
            t2 = f"({self.rvalue.get_tree()})"
        res = f"{t1} {self.op} {t2}"
        try:
            return str(eval(res))
        except NameError:
            return res

    def is_x(self):
        return self.resolved and self._value == "X"

    def contains_x(self):
        if self.resolved:
            return self._value == "X"
        else:
            return self.lvalue.contains_x() or self.rvalue.contains_x()

    def simplify(self):
        if self.resolved:
            return
        self.lvalue.simplify()
        self.rvalue.simplify()
        try:
            s = f"{self.lvalue._value} {self.op} {self.rvalue._value}"
            self._value = int(eval(s))
            self.resolved = True
            delattr(self, "lvalue")
            delattr(self, "rvalue")
        except NameError:
            pass
        except AttributeError:
            pass

    def fix_graph(self, monkeys):
        if self.resolved:
            return self
        self.lvalue = monkeys[self.lvalue]
        self.rvalue = monkeys[self.rvalue]
        self.lvalue.fix_graph(monkeys)
        self.rvalue.fix_graph(monkeys)
        return self

    def invert(self, other):
        term = other.lvalue if other.rvalue.contains_x() else other.rvalue
        if other.op == "+":
            self._value -= term._value
        if other.op == "-":
            self._value += term._value
        if other.op == "*":
            self._value = self._value // term._value
        if other.op == "/":
            self._value *= term._value
        return self._value, term

    def x_node(self):
        if self.lvalue.contains_x():
            return self.lvalue
        return self.rvalue

    def solve_for_x(self):
        x_tree = self.x_node()
        known_tree = self.rvalue if x_tree == self.lvalue else self.lvalue

        if (x_tree.op in ["*", "+"]) or \
           (x_tree.op in ["/", "-"] and x_tree.lvalue.contains_x()):
            known_tree.invert(x_tree)
            return x_tree.x_node()
        else:
            x_tree.op = "+" if x_tree.op == "-" else "*"
            x_tree.lvalue._value, known_tree._value = known_tree._value, x_tree.lvalue._value
            return x_tree


def star1():
    monkeys = [Monkey(_) for _ in data]
    monkeys = {_.name: _ for _ in monkeys}
    root = monkeys["root"].fix_graph(monkeys)
    return root.solve()


def star2():
    monkeys = [Monkey(_) for _ in data]
    monkeys = {_.name: _ for _ in monkeys}
    monkeys["root"].op = "=="
    monkeys["humn"]._value = "X"
    root = monkeys["root"].fix_graph(monkeys)
    root.simplify()

    while not any([root.lvalue.is_x(), root.rvalue.is_x()]):
        n = root.solve_for_x()
        if root.lvalue.contains_x():
            root.lvalue = n
        else:
            root.rvalue = n
    # print(root.get_tree())
    return root.rvalue._value if root.lvalue.is_x() else root.lvalue._value


print("star1:", star1())
print("star2:", star2())
