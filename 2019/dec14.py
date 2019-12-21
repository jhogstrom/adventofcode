import os
import time
import timeit

class Recipe:
    def __init__(self, r):
        materials, target = r.split(" => ")
        self.amount, self.target = target.split(" ")
        self.amount = int(self.amount)
        self.materials = {}
        materials = materials.split(", ")
        for m in materials:
            amount, material = m.split(" ")
            self.materials[material] = int(amount)

    def __str__(self):
        res = ", ".join([f"{self.materials[_]} {_}" for _ in self.materials])
        res += f" => {self.amount} {self.target}"
        return res

class NanoFactory:
    def __init__(self, recipe):
        self.recipes = {}
        self.store = {}
        for r in recipe:
            rec = Recipe(r)
            self.recipes[rec.target] = rec
            self.store[rec.target] = 0
            #print(rec)
        self.store["ORE"] = 0

    def produce(self, material):
        rec = self.recipes[material]
        #print(f"Producing {rec.amount} {material}")
        for m in rec.materials:
            self.consume(m, rec.materials[m])
        self.store[material] += rec.amount

    def consume(self, material, amount):
        if material == "ORE":
            #print(f"Using {amount} ORE")
            self.store[material] += amount
            return 

        while self.store[material] < amount:
            self.produce(material)
        self.store[material] -= amount
        assert(self.store[material] >= 0)

    def makefuel(self, amount):
        self.consume("FUEL", amount)
        print(f"{amount:>6} => {self.store['ORE']:>10} ORE")

def get_data():
    curdir = os.path.dirname(os.path.abspath(__file__))
    filename = f'{curdir}\\dec14.txt'
    prgdata = [_.strip() for _ in open(filename, 'r').readlines()]
    return prgdata

def dec14_star1():
    prgdata = ["10 ORE => 10 A",
                "1 ORE => 1 B",
                "7 A, 1 B => 1 C",
                "7 A, 1 C => 1 D",
                "7 A, 1 D => 1 E",
                "7 A, 1 E => 1 FUEL"]

    prgdata = ["9 ORE => 2 A",
                "8 ORE => 3 B",
                "7 ORE => 5 C",
                "3 A, 4 B => 1 AB",
                "5 B, 7 C => 1 BC",
                "4 C, 1 A => 1 CA",
                "2 AB, 3 BC, 4 CA => 1 FUEL"]

    prgdata = ["157 ORE => 5 NZVS",
                "165 ORE => 6 DCFZ",
                "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
                "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
                "179 ORE => 7 PSHF",
                "177 ORE => 5 HKGWZ",
                "7 DCFZ, 7 PSHF => 2 XJWVT",
                "165 ORE => 2 GPVTF",
                "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]

    prgdata = ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
                "17 NVRVD, 3 JNWZP => 8 VPVL",
                "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
                "22 VJHF, 37 MNCFX => 5 FWMGM",
                "139 ORE => 4 NVRVD",
                "144 ORE => 7 JNWZP",
                "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
                "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
                "145 ORE => 6 MNCFX",
                "1 NVRVD => 8 CXFTF",
                "1 VJHF, 6 MNCFX => 4 RFSQX",
                "176 ORE => 6 VJHF"]
    
    prgdata = ["171 ORE => 8 CNZTR",
                "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
                "114 ORE => 4 BHXH",
                "14 VRPVC => 6 BMBT",
                "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
                "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
                "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
                "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
                "5 BMBT => 4 WPTQ",
                "189 ORE => 9 KTJDG",
                "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
                "12 VRPVC, 27 CNZTR => 2 XDBXC",
                "15 KTJDG, 12 BHXH => 5 XCVML",
                "3 BHXH, 2 VRPVC => 7 MZWV",
                "121 ORE => 7 VRPVC",
                "7 XCVML => 6 RJRHP",
                "5 BHXH, 4 VRPVC => 5 LTCX"]


    prgdata = get_data()

    factory = NanoFactory(prgdata)
#    for r in factory.recipes:
#        print(factory.recipes[r])


    used_ore = []
    for amount in range(1,200):
        factory.makefuel(amount)
        used_ore.append(factory.store["ORE"])

    deltas = []
    for d in range(1, len(used_ore)):
        delta = used_ore[d] - used_ore[d-1]
        print(delta)
        deltas.append(delta)

    print("===")
    for d in range(1, len(deltas)):
        delta = deltas[d] - deltas[d-1]
        print(delta)
        #deltas.append(delta)

dec14_star1()
