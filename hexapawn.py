from copy import deepcopy
#Parminder Singh
#hexapawn

#hexapawn function line 10
#static eval on line 37
#minMaxSearch line 101
#move gen is on line 344



def hexapawn(inputBoard, boardSize, playerColor, lookAhead):
    startGame = gameSetup(inputBoard, boardSize, playerColor, lookAhead)
    head = minMaxTree(startGame)
    head.setMinMax()
    headNode = createTree(head)
    bestBoard = minMaxSearch(headNode, lookAhead)
    if bestBoard:
        return bestBoard.treeBoard.board
    else:
        return(startGame.board)

class gameSetup(object): 
    def __init__(self, board, boardSize, playerColor, lookAhead):
        self.board = board 
        self.boardSize = boardSize 
        self.playerColor = playerColor 
        self.lookAhead = lookAhead #how far to look ahead 
        self.score = self.staticEvaluation() 
        self.currentPlayer = playerColor 
        self.searchLevel = 0 #current level of tree
        
    #My static evaluation function is same as the one discussed in class slides
    #If player color piece reaches the other end of the board +10
    #If opposite of player color pieces reaches the other end of the board -10
    #Else score = number of playerpieces - number of opposite pieces
    def staticEvaluation(self):
        blackPieces = 0 
        whitePieces = 0
        whiteLost = False
        blackLost = False
        firstRow = list(self.board[0])
        lastRow = list(self.board[-1])

        #count the number of white and black pieces on board
        for row in range(self.boardSize):
            for column in range(self.boardSize):
                if (self.board[row][column] == 'b'):
                    blackPieces += 1
                if (self.board[row][column] == 'w'):
                    whitePieces += 1       
        #check wins 
        for piece in range(self.boardSize):
            if firstRow[piece] == 'b':   #if a black piece is in top row black wins!
                whiteLost = True
            elif lastRow[piece] == 'w':  #if a white piece is in botom row white wins!
                blackLost = True
        #scoring logistics
        if (self.playerColor) == 'w':
            if whiteLost == True:
                self.score = -10
            elif whiteLost == False:
                self.score = 10
            else:
                self.score = (whitePieces - blackPieces)
        elif (self.playerColor) == 'b':
            if blackLost == True:
                self.score = -10
            elif blackLost == False:
                self.score = 10
            else:
                self.score = (blackPieces - whitePieces)
        return self.score

class minMaxTree(object):
    def __init__(self, treeBoard):
        self.treeBoard = treeBoard # game should be hexapawn object
        self.parent = None
        self.children = []
        self.level = None # MIN or MAX
    
    def addChild(self, child):
        self.children.append(child)
        child.parent = self
    
    #checks if current level is a MAX or MIN needed
    #if parent is max, will return node with max score
    #if parent is min, will return node with min score
    def setMinMax(self):
        if (self.parent):
            if(self.parent.level == 'MAX'):
                self.level = 'MIN'
            else:
                self.level = 'MAX'
        else: 
            self.level = 'MAX'

# minimax search
#input needed is the head node from the createTree function.
#outputs either the max value or the min value depending on which layer it is in.
def minMaxSearch(head, lookAhead):
    if (head.treeBoard.searchLevel < lookAhead - 1):
        if(head.children != []):
            for i in range(len(head.children)):
                if (head.children[i].treeBoard.score == -10):
                    break # LOST no need to further search
                if (head.children[i].treeBoard.score == 10):
                    break  # WIN no need to further search
                minMaxSearch(head.children[i], lookAhead)
        else: 
            return 
    if(head.level == 'MAX'):
        maxValue = -10 #lowest a max could be techincally
        maxBoard = head.children[0]
        for i in range(len(head.children)):
            if (head.children[i].treeBoard.score > maxValue): #if the current score i > previous minValue, update the board and the minvalue
                maxBoard = head.children[i]
                maxValue = head.children[i].treeBoard.score
        head.treeBoard.score = maxBoard.treeBoard.score
        head.children.clear() 
        return maxBoard
    if(head.level == 'MIN'):
        minValue = 10 #highest a min can be technically
        minBoard = head.children[0]
        for i in range(len(head.children)):
            if(head.children[i].treeBoard.score < minValue): #if the current score i < previous minValue, update the board and the minvalue
                minBoard = head.children[i]
                minValue = head.children[i].treeBoard.score
        head.treeBoard.score = minBoard.treeBoard.score
        head.children.clear() 
        return minBoard

# tree used in the minMaxSearch function
def createTree(head):
    if(head.treeBoard.lookAhead > 0):
        nextLevel = moveGenerator(head.treeBoard)
        for i in range(len(nextLevel)):
            next = minMaxTree(nextLevel[i])
            head.addChild(next)
            next.setMinMax()
            next.treeBoard.lookAhead = head.treeBoard.lookAhead - 1
            next.treeBoard.searchLevel = head.treeBoard.searchLevel + 1
        for j in range(len(head.children)):
            createTree(head.children[j])
    elif (head.treeBoard.lookAhead == 0):
        return
    return head

#finds the white and black pieces on the voard
#returns the row and column tuple of target color
def findPieces(currBoard, target):
    size = currBoard.boardSize
    board = currBoard.board.copy()
    whitePieces = []
    blackPieces = []
    for row in range(size):
        for column in range(size):
            if board[row][column] == 'w':
                whitePieces.append((column,row)) 
            if board[row][column] == 'b':
                blackPieces.append((column,row)) 
    if(target == 'b'):
        return blackPieces
    elif (target == 'w'):
        return whitePieces
    else:
        return None

#MOVEMENT--------------------------------------------------
#all movement functions get the current board state and iterates over a column and row.
#inputs are the current board, column and row
#the column and row inputs are coming in from the whiteStates and blackStates functions

def moveWhiteDown(currBoard, column, row):
    board = (currBoard.board).copy()
    if(board[row][column] != 'w'):
        return None
    if ((row + 1) >= currBoard.boardSize): #check scope
        return None
    # check  under the white piece
    if (board[row + 1][column] == '-'):
        whiteInitialRow = list(board[row]) 
        whiteInitialRow[column]= '-'
        moveWhiteToBlank = list(board[row + 1])
        moveWhiteToBlank[column] = 'w'
        string1 = ''.join(moveWhiteToBlank) #convert to string
        string2 = ''.join(whiteInitialRow)  #convert to string
        # replace in board
        board[row] = string2 # puts the blank spot on the initial row
        board[row + 1] = string1 ## puts the  white piece on the row under it.
    else:
        return None
    return board

def moveBlackUp(currBoard, column, row):
    board = (currBoard.board).copy()
    if(board[row][column] != 'b'):
        return None
    if ((row - 1) < 0):
        return None
        #check above the black piece
    if (board[row - 1][column] == '-'):
        blackInitialRow = list(board[row]) 
        blackInitialRow[column]= '-'
        moveBlackToBlank = list(board[row - 1])
        moveBlackToBlank[column] = 'b'
        string1 = ''.join(moveBlackToBlank) #convert to string 
        string2 = ''.join(blackInitialRow) #convert to string   
        board[row] = string2        # puts the blank spot on the initial row
        board[row - 1] = string1    # puts the  black piece on the row above it.
    else:
        return None
    return board

def moveWhiteDiagonalLeft(currBoard, column, row):
    board = (currBoard.board).copy()
    if (board[row][column] != 'w'):
        return None
    if((column - 1) < 0) or ((row + 1) >= currBoard.boardSize): #check scope
        return None
    if(board[row + 1][column - 1] == 'b'):
        changeToBlank = list(board[row])
        changeToBlank[column] = '-'
        changeToWhite = list(board[row + 1])
        changeToWhite[column - 1] = 'w'
        string1 = ''.join(changeToBlank) #convert to string 
        string2 = ''.join(changeToWhite)#convert to string 
        board[row] = string1
        board[row + 1] = string2
        return board
    else: 
        return None

def moveWhiteDiagonalRight(currBoard, column, row):
    board = (currBoard.board).copy()
    if (board[row][column] != 'w'):
        return None
    if((column + 1) >= currBoard.boardSize) or ((row + 1) >= currBoard.boardSize): #check scope
        return None
    if(board[row + 1][column + 1] == 'b'):
        changeToBlank = list(board[row])
        changeToBlank[column] = '-'
        changeToWhite = list(board[row + 1])
        changeToWhite[column + 1] = 'w'
        string1 = ''.join(changeToBlank)
        string2 = ''.join(changeToWhite)
        board[row] = string1
        board[row + 1] = string2
        return board
    else: 
        return None

def moveBlackDiagonalLeft(currBoard, column, row):
    board = (currBoard.board).copy()
    if (board[row][column] != 'b'):
        return None
    if ((column - 1) < 0) or ((row + 1) < 0): #check scope
        return None
    if(board[row - 1][column - 1] == 'w'):
        changeToBlank = list(board[row])
        changeToBlank[column] = '-'
        changeToWhite = list(board[row - 1])
        changeToWhite[column - 1] = 'b'
        string1 = ''.join(changeToBlank)
        string2 = ''.join(changeToWhite)
        board[row] = string1
        board[row - 1] = string2
        return board
    else: 
        return None

def moveBlackDiagonalRight(currBoard, column, row):
    board = (currBoard.board).copy()
    if (board[row][column] != 'b'):
        return None
    if ((column + 1) >= currBoard.boardSize) or ((row - 1) < 0): #check scope
        return None
    if (board[row - 1][column + 1] == 'w'):
        changeToBlank = list(board[row])
        changeToBlank[column] = '-'
        changeToWhite = list(board[row - 1])
        changeToWhite[column + 1] = 'b'
        string1 = ''.join(changeToBlank)
        string2 = ''.join(changeToWhite)
        board[row] = string1
        board[row - 1] = string2
        return board
    else:
        return None

#stATes----------------------------------------------------------

def whiteStates(white,currBoard):
    states = []
    for i in range(len(white)):
        down = moveWhiteDown(currBoard, white[i][0], white[i][1])
        right = moveWhiteDiagonalRight(currBoard, white[i][0], white[i][1])
        left = moveWhiteDiagonalLeft(currBoard, white[i][0], white[i][1])
        if(down):
            downStates = gameSetup(down,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            downStates.currentPlayer = 'b'
            states.append(downStates)
        if(right):
            rightStates = gameSetup(right,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            rightStates.currentPlayer = 'b'
            states.append(rightStates)
        if(left):
            leftStates = gameSetup(left,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            leftStates.currentPlayer = 'b'
            states.append(leftStates)
    if (states == []):
        if (currBoard.currentPlayer == currBoard.playerColor):
            currBoard.score = -10
        else:
            currBoard.score = 10
    return states


def blackStates(black,currBoard):
    states = []
    for i in range(len(black)):
        up = moveBlackUp(currBoard, black[i][0], black[i][1])
        right = moveBlackDiagonalRight(currBoard, black[i][0], black[i][1])
        left = moveBlackDiagonalLeft(currBoard, black[i][0], black[i][1])
        if(up):
            upStates = gameSetup(up,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            upStates.currentPlayer = 'w'
            states.append(upStates)
        if(right):
            rightStates = gameSetup(right,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            rightStates.currentPlayer = 'w'
            states.append(rightStates)
        if(left):
            leftStates = gameSetup(left,currBoard.boardSize,currBoard.playerColor,currBoard.lookAhead)
            leftStates.currentPlayer = 'w'
            states.append(leftStates)
    if (states == []):
        if (currBoard.currentPlayer == currBoard.playerColor):
            currBoard.score = -10
        else:
            currBoard.score = 10
    return states

def moveGenerator(currBoard):
    if (currBoard.currentPlayer == 'w'):
        white = findPieces(currBoard, 'w')
        states = whiteStates(white,currBoard)
    else:
        black = findPieces(currBoard, 'b')
        states = blackStates(black,currBoard)
    return states 


hexapawn(["www","---","bbb"],3,'w',2)
#hexapawn(["www","---","bbb"],3,'w',2)