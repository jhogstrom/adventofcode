import os


def get_records(data):
    res = []
    for s in data:
        if s != "":
            res.append(s)
        else:
            if res != [""] and res != []:
                yield res
            res = []

    if res != [] and res != [""]:
        yield res


def get_data(srcfilename, *, converter = str, extra=""):
    filename = os.path.abspath(srcfilename).replace(".py", extra+".txt")
    if not os.path.exists(filename):
        raise Exception(f"'{filename} does not exist")
    return [converter(_.strip()) for _ in open(filename, 'r').readlines()]