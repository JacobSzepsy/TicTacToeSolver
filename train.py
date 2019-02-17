import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import keras
import numpy as np
class tic_tac_toe:
    def __init__(self):
	self.board = list(range(1,10))
	self.gameState = 0
	#X is 1 O is 2
	self.playerState = 1
    
#turn state
    def draw(self):
        print(self.board[0], self.board[1], self.board[2])
        print(self.board[3], self.board[4], self.board[5])
        print(self.board[6], self.board[7], self.board[8])
        print()

    def is_game_over(self):
        for a, b, c in WIN_COMBINATIONS:
            if self.board[a] == self.board[b] == self.board[c]:
                if self.board[a] == 'X':
                    self.gameState = 1
                else:
                    self.gameState = 2
                return True
        if 9 == sum((pos == 'X' or pos == 'O') for pos in self.board):
            self.gameState = 3
            return True
    def getBoard(self):
        return self.board
	
    def setBoard(self, board):
	self.board = board
        WIN_COMBINATIONS = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6),]
        for a,b,c in WIN_COMBINATIONS:
            if self.board[a] == self.board[b] == self.board[c]:
                if self.board[a] == 'X':
                    self.gameState=1
                else:
                    self.gameState = 2
                break
            elif self.board.count('X') + self.board.count('O') == 9:
                self.gameState = 3
                break
	
    def getPlayerState(self):
	return self.playerState
	
    def setPlayerState(self, state):
	self.playerState = state
	
    def getGameState(self):
	return self.gameState
def posMovs(board, playerState):
    moves = []
    for i in range(9):
	if board[i] != 'X' and board[i] != "O":
            temp = list(board)
            if playerState == 1:
                temp[i] = 'X'
            elif playerState == 2:
                temp[i] = 'O'
            moves.append(temp)
    return moves
	
def convert(data):
    out = [0] * 18
    for i in range(9):
        if data[i] == 'O':
            out[i] = 1
        elif data[i] == 'X':
            out[i+9] = 1
    return np.asarray(out)

def shift(array, value):
	newArray = []
	for i in range(1,len(array)):
		newArray.append(array[i])
	newArray.append(value)
	return newArray
#Initializes NN model
network = Sequential()
#input layer that looks at the board in terms of 'O' placements, 'X' placements, and empty spots respectively
#Sample input: 100000000,001000000
network.add(Dense(
    18,
    input_shape=(18,),
    kernel_initializer='random_uniform'
    ))
#output layer that generates a score based on the board placement
network.add(Dense(
    1,
    #output_dim=1,
    kernel_initializer='random_uniform'
    ))
opt = SGD(lr = 0.001, momentum = 0.5, nesterov = False)
network.compile(
        loss='mean_squared_error',
        optimizer = opt,
        )
network.summary()
def selectMove(board, playerState):
    scores = []
    moves = posMovs(board, playerState)
    if playerState == 1:
        for move in moves:
            score = network.predict(np.asarray([convert(move)]))
            scores.append(score)
            
        return moves[scores.index(max(scores))],max(scores)
    elif playerState == 2:
        return random.choice(moves)

def train(network):
    game = tic_tac_toe()
    moveList = []
    scoreList = []
    while(True):
        if game.getGameState() == 0:
	    if game.getPlayerState() == 1:
	        board,score = selectMove(game.getBoard(), game.getPlayerState())
                moveList.append(convert(board))
		scoreList.append(score)
		game.setBoard(board)
	        game.setPlayerState(2)
	    elif game.getPlayerState() == 2:
		game.setBoard(random.choice(posMovs(game.getBoard(), game.getPlayerState())))
                game.setPlayerState(1)
	elif game.getGameState() == 1:
	    scoreList = shift(scoreList, 1)
            break
	elif game.getGameState() == 2:
	    scoreList = shift(scoreList, -1)
            break
        elif game.getGameState() == 3:
	    scoreList = shift(scoreList, 0)
            break
    network.fit(np.asarray(moveList), np.asarray(scoreList), epochs = 1, verbose=0)
    return network, game.getGameState()
winCount = 0
lossCount = 0
drawCount = 0
for i in range(20000):
    network,result = train(network)
    if result == 1:
        winCount += 1
    elif result == 2:
        lossCount += 1
    elif result == 3:
        drawCount += 1	
    if i % 1000 == 0 and i != 0:
        print("game number",i,'win percentage',winCount,"loss count", lossCount, "draw count", drawCount)
network.save('TTTmodel.h5')
