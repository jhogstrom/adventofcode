from collections import defaultdict
#452 players; last marble is worth 71250 points

players, marbles, hs = 452, 71250, -1

#players, marbles, hs = 9, 25, 32
#players, marbles, hs = 10, 1618, 8317
#players, marbles, hs = 13, 7999, 146373
#players, marbles, hs = 17, 1104, 2764
#players, marbles, hs = 21, 6111, 54718
#players, marbles, hs = 30, 5807, 37305

board = [0]
score = defaultdict(int)
currentpos = 0
player = -1

def printboard(b, cp, p, pl):
	r = "[{0:3}] ".format(pl)
	for i in range(len(b)):
#	for i in b:
		if i == cp:
			r += " ({0:2})".format(b[i])
		else:
			r += "  {0:2} ".format(b[i])
	print(r, "---", cp)

printboard(board, currentpos, 0, player)
for i in range(1, marbles+1):
	if i % 1000 == 0:
		print(i)
	player = (player + 1) % (players)
	if i % 23 == 0:
		#print("mod 23! <=", i)
		# 
		score[player] += i
		m2pos = (currentpos + len(board) - 7) % len(board)
		score[player] += board[m2pos]
#		print("player {0} got {1} + {2} = {3}".format(player+1, i, board[m2pos], i + board[m2pos]))
		board = board[:m2pos] + board[m2pos+1:]
		# Remove m2pos from board
		#...
		currentpos = m2pos #+ ) % len(board))
	else:
		currentpos += 2
		if currentpos  > len(board):
			currentpos = 1
		board = board[:currentpos] + [i] + board[currentpos:]	
		currentpos = board.index(i)
	#printboard(board, currentpos, i, player + 1)


print("high score=", max(score.values()))
print("Expected  =", hs)