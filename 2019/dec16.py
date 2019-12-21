rawdata = "59780176309114213563411626026169666104817684921893071067383638084250265421019328368225128428386936441394524895942728601425760032014955705443784868243628812602566362770025248002047665862182359972049066337062474501456044845186075662674133860649155136761608960499705430799727618774927266451344390608561172248303976122250556049804603801229800955311861516221350410859443914220073199362772401326473021912965036313026340226279842955200981164839607677446008052286512958337184508094828519352406975784409736797004839330203116319228217356639104735058156971535587602857072841795273789293961554043997424706355960679467792876567163751777958148340336385972649515437"

inputsignal = "12345678"

class FFT:
    def __init__(self, data):
        self.data = [int(_) for _ in data]
        self.pattern = [int(_) for _ in "0, 1, 0, -1".split(", ")]
        self.patterns = None
        start = int(data[:7])
        #start = len(data*2)
        #offset = start % len(data)
        offset = start
        print(f"Start: {start} Length= {len(data)} Offset%: {offset}")
        self.offset = offset

    def genpattern(self, n):
        p = {}
        c = 0
        while len(p) <= len(self.data) + 1:
            for i in range(len(self.pattern)):
                for r in range(n+1):
                    pat = self.pattern[i%len(self.pattern)]
                    p[c] = pat
                    c += 1

                if len(p) > len(self.data)+1:
                    break
        return p

    def get_expensive_multiplier(self, row, pos):
        if self.patterns == None:
            self.patterns = self.generate_patterns()
        return self.patterns[row][pos]

    def get_multiplier(self, row, pos):
        #exp_m = self.get_expensive_multiplier(row, pos)
        #return exp_m

        period = (row+1) * len(self.pattern)
        offset = pos % period
        target = offset // (row+1)
        return self.pattern[target]


    def generate_patterns(self):
        res = []
        print(f"Generating {len(self.data)} patterns...")
        for i in range(len(self.data)):
            res.append(self.genpattern(i))
            #print(f"Pattern {i}")
            #sleep(2)
        return res

    def transform(self, rounds):
        for r in range(rounds):  
            newdata = []
            for i in range(len(self.data)):
                s = 0
                for n in range(len(self.data)):
                    multiplier = self.get_multiplier(i, n+1)
                    if multiplier == 0:
                        continue
                    if multiplier == 1:
                        s += self.data[n]
                        continue
                    if multiplier == -1:
                        s -= self.data[n]
                    #print(f"{o:>2}*{multiplier:>2} + ", end = "")
                s = int(str(s)[-1])
                newdata.append(s)
                #print()
            self.data = newdata
            print("".join([str(_) for _ in newdata[:8]]))
            #print("===")

def dec16_star1():
    f = FFT(rawdata * 100)
#    for row in range(len(f.data)):
#       for p in range(1, len(f.data)):
#            f.get_multiplier(row, p)

#    exit()
    #print(f.genpattern(0))
    #print(f.genpattern(1))
    #print(f.genpattern(2))
    #print(f.genpattern(3))
    #print(f.genpattern(4))
    f.transform(100)

    print(f"Using offset {f.offset:>7}: {'-'.join([str(_) for _ in f.data[f.offset:f.offset+8]])}")
    print(f"Using offset {0:>7}: {'-'.join([str(_) for _ in f.data[:8]])}")

dec16_star1()
