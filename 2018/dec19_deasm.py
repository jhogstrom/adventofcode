
reg[3] += 16 # (00) addi 3 16 3 
reg[4] = 1 # (01) seti 1 3 4
reg[5] = 1 # (02) seti 1 8 5
reg[1] = reg[4] * reg[5] # (03) mulr 4 5 1

reg[1] = 1 if reg[1] == reg[2] else 0 # (04) eqrr 1 2 1
reg[3] += reg[1] # (05) addr 1 3 3
reg[3] +=  1 # (06) addi 3 1 3
reg[0] += reg[4]  # (07) addr 4 0 0
reg[5] += 1 # (08) addi 5 1 5
reg[1] = 1 if reg[5] > reg[2] else 0 # (09) gtrr 5 2 1
reg[3] += reg[1] # (10) addr 3 1 3
reg[3] = 2 # (11) seti 2 6 3
reg[4] += 1 # (12) addi 4 1 4

reg[1] = 1 if reg[4] > reg[2] else 0 # (13) gtrr 4 2 1
reg[3] += reg[1] # (14) addr 1 3 3
reg[3] = 1 # (15) seti 1 1 3
reg[3] = reg[3] * reg[3] # (16) mulr 3 3 3

reg[2] += 2 # (17) addi 2 2 2
reg[2] = reg[2] * reg[2] # (18) mulr 2 2 2
reg[2] = reg[3] * reg[2] # (19) mulr 3 2 2
reg[2] *= 11 # (20) muli 2 11 2
reg[1] += 5 # (21) addi 1 5 1
reg[1] *= reg[3] # (22) mulr 1 3 1
reg[1] += 8 # (23) addi 1 8 1
reg[2] += reg[1] # (24) addr 2 1 2
reg[3] += reg[0] # (25) addr 3 0 3
reg[3] = 0 # (26) seti 0 5 3
reg[1] = reg[3] # (27) setr 3 9 1
reg[1] *= reg[3] # (28) mulr 1 3 1
reg[1] += reg[3] # (29) addr 3 1 1
reg[1] *= reg[3] # (30) mulr 3 1 1
reg[1] *= 14 # (31) muli 1 14 1
reg[1] *= reg[3] # (34) mulr 1 3 1
reg[2] += reg[1] # (33) addr 2 1 2
reg[0] = 0 # (34) seti 0 9 0
reg[3] = 0 # (35) seti 0 9 3
