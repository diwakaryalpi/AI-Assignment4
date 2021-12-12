import random
from copy import deepcopy #deepcopy library is used so that the content can be copied recursively

#initializing the values
originalBoard=[]
baseScore = 100000 

def initBoard(m,n):
    for i in range(n):
        temp=[]
        for j in range(m):
            temp.append(' ')
        originalBoard.append(temp)


def printBoard(board):        #For printing the connect4 board to understand moves
    print "\n"
    for i in range(n):
        for j in range(m):
            print "| "+board[i][j],
        print "|"
        print " "+"-"*(4*m-1)
    print "\n"

print "AI - X\nYou - O\n" #Computer puts X and the player has to use 0 to play

def assignStartingPlayer():   #Function to select who plays first
    temp = random.randint(0,10)
    return 'X' if temp%2==0 else 'O'


m=7 # number of columns of the connect4 board
n=6 # number of rows of the connect4 board
initBoard(m,n)
startPlayer = assignStartingPlayer()
# printBoard()

def isGameOver(board,depth,score):    # Function to see if there are any available possible moves
    availableMoves = getAvailableStates(board)
    countValidMoves = 0
    for i in availableMoves:
        if i!=-1:
            countValidMoves+=1
# if this node (state) is a terminal node or depth == 0 or if there are no valid moves left
    if depth == 0 or score==baseScore or score==-baseScore or countValidMoves==0:
        return True
    # print "returning false"
    return False

#evaluation function is defined
def evaluation_function(self, state):
        if self.current_move == 0:
            o_color = X
        elif self.current_move == X:
            o_color = 0
        my_fours = self.checkForStreak(state, self.bestmove, 4)
        my_threes = self.checkForStreak(state, self.bestmove, 3)
        my_twos = self.checkForStreak(state, self.bestmove, 2)
        comp_fours = self.checkForStreak(state, o_color, 4)
        comp_threes = self.checkForStreak(state, o_color, 3)
        comp_twos = self.checkForStreak(state, o_color, 2)
        return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)

def checkForStreak(self, state, color, streak):
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalStreak(i, j, state, streak)
                    count += self.horizontalStreak(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

def verticalStreak(self, row, column, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

def horizontalStreak(self, row, column, state, streak):
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

def diagonalCheck(self, row, column, state, streak):
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total


def getAvailableStates(board):
    temp=[-1]*m
    for i in range(n):
        for j in range(m):
            if board[i][j]==' ':
                temp[j]=i
    return temp

def individualScore(board,r,c,d_y,d_x): #Function to get the individual scores of the players
    # printBoard(board)
    hp = 0
    cp = 0
    for i in range(4):
        if board[r][c] == "O":
            hp+=1
        elif board[r][c] == "X":
            cp+=1
        r += d_y
        c += d_x

    if hp == 4:
        return -baseScore
    elif cp == 4:
        return baseScore
    else:
        return cp


def getScore(board): #For calculating the scores of the players

    totalPoints = 0
    for row in range(n-3):
        for column in range(m):
            score = individualScore(board,row, column, 1, 0)
            if score == baseScore:
                return baseScore
            if score == -baseScore:
                return -baseScore
            totalPoints += score


    for row in range(n):
        for column in range(m-3):
            score = individualScore(board,row, column, 0, 1)
            if score == baseScore:
                return baseScore
            if score == -baseScore:
                return -baseScore
            totalPoints += score

    for row in range(n-3):
        for column in range(m-3):
            score = individualScore(board,row, column, 1, 1)
            if score == baseScore:
                return baseScore
            if score == -baseScore:
                return -baseScore
            totalPoints += score

    for row in range(n):
        for column in range(m-3):
            score = individualScore(board,row, column, -1, 1)
            if score == baseScore:
                return baseScore
            if score == -baseScore:
                return -baseScore
            totalPoints += score

    return totalPoints

#For using minimax algorithm using the below functions maximize and minimize are defined

def maximize(depth,board): #this function gives the maximum 

    score = getScore(board)
    if isGameOver(board,depth,score):
        return [-1, score]

    maxi = [-1,-99999]

    availableMoves = getAvailableStates(board)
    for i in range(len(availableMoves)):
        if availableMoves[i]!=-1:
            tempBoard = deepcopy(board)
        
            tempBoard[availableMoves[i]][i] = "X"
# if the program is unable to get best move using maximize function, it uses minimize function to know the best move
            bestMove = minimize(depth-1,tempBoard) 

            if maxi[0]==-1 or bestMove[1] > maxi[1]:
                maxi[0] = i
                maxi[1] = bestMove[1]
    return maxi


def minimize(depth,board):


    if isGameOver(board, depth,score):
        return [-1, score]
    mini = [-1,99999]

    availableMoves = getAvailableStates(board)
    for i in range(len(availableMoves)):
#         print "aasdsds"
        if availableMoves[i]!=-1:

            tempBoard = deepcopy(board)
            
            tempBoard[availableMoves[i]][i] = "O"
# if the program is unable to get best move using minimize function, it uses maximize function to know the best move
            bestMove = maximize(depth-1,tempBoard)

            if mini[0]==-1 or bestMove[1] < mini[1]:
                mini[0] = i
                mini[1] = bestMove[1]

            # tempBoard[availableMoves[i]][i] = " "

    return mini
    

print 'Computer is starting first\n' if startPlayer=='X' else 'You are starting first\n'
player = 'O'

depth = 4


score = getScore(originalBoard)

while not isGameOver(originalBoard,depth,score) or isGameOver(originalBoard,depth,score):
    if player=='O': 
        availableMoves = getAvailableStates(originalBoard)                    # once we find the first empty, we know it's a legal move
        humanMove = input('Your turn. Enter a column between 1 and '+str(m)+' : ')
        while int(humanMove)<1 or int(humanMove)>m:                           # To check if the user has entered the valid number
            print "Enter a valid move",
            humanMove = input('Your turn. Enter a column between 1 and '+str(m)+' : ')
        while availableMoves[humanMove-1]==-1:                               #To check if there are no available moves in a column
            print "Column "+str(humanMove)+" is already full"
            humanMove = input('Choose another column : ')
            while int(humanMove)<1 or int(humanMove)>m:                      # To check if the user has entered the valid number
                print "Enter a valid move",
                humanMove = input('Your turn. Enter a column between 1 and '+str(m)+' : ')

        originalBoard[availableMoves[humanMove-1]][humanMove-1]='O'
        player='X'
    else:
        bestMove = maximize(depth,originalBoard)
        
        availableMoves = getAvailableStates(originalBoard)
        
        originalBoard[availableMoves[bestMove[0]]][bestMove[0]] = 'X'
        player = 'O'
        print "Computer made a move"
        printBoard(originalBoard)
        
        
    score = getScore(originalBoard)
    if isGameOver(originalBoard, depth, score):
    	if score==baseScore:
    		print "AI won"
#               return evaluation_function(originalBoard, depth)
    	elif score==-baseScore:
    		print "You won"
    	exit()

print "Game over"
