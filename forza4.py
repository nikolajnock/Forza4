import numpy as np
import pandas as pd
import time

np.random.seed(2)  # reproducible


EMPTY = 0
RED_COIN = 1
YELLOW_COIN = 2

ACTIONS = ['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7']
N_COLUMNS = len(ACTIONS)
N_ROWS = 6

GAME_IS_ONGOING = 0
RED_WINS = 1
YELLOW_WINS = 2
DRAW = 3

    
zeroState = np.zeros( ( N_ROWS, N_COLUMNS ), np.int8 )

def getColumn(state, col):
    return state[:,col]

def countCoinsInColumn( state, col ):
    col = getColumn(state, col)
    return np.count_nonzero(col)

def columnIsFull( state, col ):
    return countCoinsInColumn(state,col) == 0

def throwCoin( state, col, coin ):
    num_of_coins = countCoinsInColumn( state, col )
    if num_of_coins < N_ROWS:
        row = N_ROWS - num_of_coins - 1
        state[row][col] = coin
        return True
    else:
        return False

    
def checkColumns(state):
    for col in range(N_COLUMNS):
        column = getColumn(state,col)
        counter = [0,0,0]
        for row in range(N_ROWS - 4 + 1 ):
            if column[row] == EMPTY:
                counter = [0,0,0]
            elif column[row] == RED_COIN:
                counter[RED_COIN] += 1
                counter[YELLOW_COIN] = 0
            elif column[row] == YELLOW_COIN:
                counter[RED_COIN] = 0
                counter[YELLOW_COIN] += 1
            if counter[RED_COIN] == 4:
                return RED_WINS
            elif counter[YELLOW_COIN] == 4:
                return YELLOW_WINS
    return GAME_IS_ONGOING

def checkRows(state):
    for row in range(N_ROWS):
        current_row = state[row,:]
        counter = [0,0,0]
        for col in range(N_COLUMNS - 4 + 1 ):
            if current_row[col] == EMPTY:
                counter = [0,0,0]
            elif current_row[col] == RED_COIN:
                counter[RED_COIN] += 1
                counter[YELLOW_COIN] = 0
            elif current_row[col] == YELLOW_COIN:
                counter[RED_COIN] = 0
                counter[YELLOW_COIN] += 1
            if counter[RED_COIN] == 4:
                return RED_WINS
            elif counter[YELLOW_COIN] == 4:
                return YELLOW_WINS
    return GAME_IS_ONGOING

def getDown4Diagonal( state, row, col ):
    diagonal = []
    for l in range(4):
        r = row + l
        c = col + l
        if r < N_ROWS and c < N_COLUMNS:
            diagonal.append( state[r,c] )
        else:
            break
    return diagonal

def getUp4Diagonal( state, row, col ):
    diagonal = []
    for l in range(4):
        r = row - l
        c = col + l
        if r >= 0 and c < N_COLUMNS:
            diagonal.append( state[r,c] )
        else:
            break
    return diagonal

def checkUpDiagonals(state):
    for row in range( 3, N_ROWS ):
        for col in range( N_COLUMNS - 4 + 1 ):
            up_diagonal = getUp4Diagonal( state, row, col )
            counter = [0,0,0]
            for coin in up_diagonal:
                counter[coin] += 1
            if counter[RED_COIN] == 4:
                return RED_WINS
            elif counter[YELLOW_COIN] == 4:
                return YELLOW_WINS
    return GAME_IS_ONGOING

def checkDownDiagonals(state):
    for row in range( N_ROWS ):
        for col in range(N_COLUMNS - 4 + 1 ):
            down_diagonal = getDown4Diagonal4( state, row, col )
            counter = [0,0,0]
            for coin in down_diagonal:
                counter[coin] += 1
            if counter[RED_COIN] == 4:
                return RED_WINS
            elif counter[YELLOW_COIN] == 4:
                return YELLOW_WINS
    return GAME_IS_ONGOING



def checkState(state):
    situation = checkRows(state)
    if situation != GAME_IS_ONGOING:
        return situation
    situation = checkColumns(state)
    if situation != GAME_IS_ONGOING:
        return situation
    situation = checkUpDiagonals(state)
    if situation != GAME_IS_ONGOING:
        return situation
    situation = checkDownDiagonals(state)
    if situation != GAME_IS_ONGOING:
        return situation
    
    number_of_coins = np.count_nonzero(state)
    if number_of_coins == N_COLUMNS * N_ROWS:
        return DRAW
    return GAME_IS_ONGOING

def createStateKey(state):
    key = ""
    for r in range(N_ROWS):
        row = state[r,:]
        last_coin = EMPTY
        counter = 0
        for c in range(N_COLUMNS):
            coin = row[c]
            is_first_column = c == 0
            is_last_column = c+1 == N_COLUMNS
            if is_first_column:
                last_coin = coin
                counter = 1
            elif coin == last_coin:
                counter += 1
            elif coin != last_coin:
                link = (counter << 4) | last_coin
                print( "row", row, "counter", counter, "last_coin", last_coin )
                key = key + str(chr(link))
                last_coin = coin
                counter = 1
            if is_last_column:
                link = (counter << 4) | last_coin
                print( "row", row, "counter", counter, "last_coin", last_coin )
                key = key + str(chr(link))
                last_coin = coin
                counter = 0
    return key

def get_env_feedback( state, action, coin ):
    """
    action action = column index, 0..6
    coin coin = RED/YELLOW
    """
    # This is how agent will interact with the environment
    
    reward = 0
    assert not columnIsFull( state, action )
    throwCoin( state, action, coin )
    state_ = state
    status = checkState(state)
    if status == RED_WINS or status == YELLOW_WINS:
        win = status == coin
        if win:
            reward = +1
        else:   #lose
            reward = -1
    return state_, reward
    


k = createStateKey(zeroState)
d = {k: [0,0,0,0,0,0,0] }
print(d)
    


s = zeroState.copy()
print(createStateKey(s))
column = getColumn(s,1)
print(s)
print(column)

throwCoin( s, 1, RED_COIN )
k2 = createStateKey(s)
print(k2)

print(s)
d[k2] = [0,1,0,2,0,3,0]

print(d)




