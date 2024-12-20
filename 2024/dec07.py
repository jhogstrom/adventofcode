import logging

from reader import get_data, set_logging, timeit

runtest = False
stardate = "07"
year = "2024"

set_logging(runtest)
data = get_data(stardate, year, runtest)
data2 = data[:]


# def evaluate(expected_value: int, lvalue: int, terms: list[int], ops: list[str]) -> int:
#     if not terms:
#         return lvalue if lvalue == expected_value else 0
#     if lvalue > expected_value:
#         return 0
#     for o in ops:
#         if o == "+":
#             next_lvalue = lvalue + terms[0]
#         elif o == "*":
#             next_lvalue = lvalue * terms[0]
#         elif o == "||":
#             next_lvalue = int(str(lvalue) + str(terms[0]))
#         else:
#             raise ValueError(f"Unknown operator '{o}'")
#         res = evaluate(expected_value, next_lvalue, terms[1:], ops)
#         if res == expected_value:
#             return res
#     return 0


def evaluate(
    expected_value: int, lvalue: int, terms: list[int], allow_concat: bool = False
) -> bool:
    if not terms:
        return lvalue == expected_value
    if lvalue > expected_value:
        return False
    next_terms = terms[1:]
    t0 = terms[0]
    return (
        evaluate(expected_value, lvalue + t0, next_terms, allow_concat)
        or evaluate(expected_value, lvalue * t0, next_terms, allow_concat)
        or (
            allow_concat
            and evaluate(
                expected_value, int(str(lvalue) + str(t0)), next_terms, allow_concat
            )
        )
    )


def parse(s: str) -> tuple[int, list[int]]:
    x = s.split()
    expected_value = int(x[0][:-1])
    terms = [int(_) for _ in x[1:]]
    return expected_value, terms


@timeit
def star1(data):
    logging.debug("running star 1")
    result = 0
    for s in data:
        expected_value, terms = parse(s)
        if evaluate(expected_value, terms[0], terms[1:]):
            result += expected_value
    print(result)


@timeit
def star2(data):
    pass
    logging.debug("running star 2")
    result = 0
    for s in data:
        expected_value, terms = parse(s)
        if evaluate(expected_value, terms[0], terms[1:]):
            result += expected_value
        elif evaluate(expected_value, terms[0], terms[1:], True):
            result += expected_value
    print(result)


star1(data)
star2(data2)
