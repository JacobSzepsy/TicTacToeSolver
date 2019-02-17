import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.models import load_model
import numpy as np
class tic_tac_toe:
    def __init__(self):
        self.board = list(range(1,10))
        self.gameState = 0
        #X is 1 O is 2
        self.playerState = 1
    
#turn state
    def draw(self):
        print(str(self.board[0]), str(self.board[1]),str(self.board[2]))
        print(str(self.board[3]), str(self.board[4]), str(self.board[5]))
        print(str(self.board[6]), str(self.board[7]), str(self.board[8]))
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
network = load_model('TTTmodel.h5')
def selectMove(board, playerState):
    scores = []
    moves = posMovs(board, playerState)
    if playerState == 1:
        for move in moves:
            score = network.predict(np.asarray([convert(move)]))
            scores.append(score)
            
        return moves[scores.index(max(scores))]
    elif playerState == 2:
        print("where would you like to move")
        while(True):
            a = int(input())
            a -= 1
            if board[a] != 'X' and board[a] != 'O':
                board[a] ='O'
                break
            else:
                print("Move is not valid")
        return board
def play(network):
    game = tic_tac_toe()
    while(True):
        if game.getGameState() == 0:
            if game.getPlayerState() == 1:
                board = selectMove(game.getBoard(), game.getPlayerState())
                game.setBoard(board)
                game.draw()
                game.setPlayerState(2)
            elif game.getPlayerState() == 2:
                selectMove(game.getBoard(), game.getPlayerState())
                game.setBoard(board)
                game.draw()
                game.setPlayerState(1)
        elif game.getGameState() == 1:
            print('You lost!')
            break
        elif game.getGameState() == 2:
            print('You Win!')
            break
        elif game.getGameState() == 3:
            print('It\'s a draw!')
            break
play(network)
