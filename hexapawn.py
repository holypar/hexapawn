#Parminder Singh
#hexapawn

def hexapawn(inputBoard, boardSize, playerColor, lookAhead):
    startGame = gameSetup(inputBoard, boardSize, playerColor, lookAhead)
    head = minMaxTree(startGame)
    head.setMinMax()
    headNode = createTree(head)
    bestBoard = minMaxSearch(headNode, lookAhead)
    if (bestBoard):
        return bestBoard.board.board
    else:
        return(startGame.board)



class gameSetup(object):
    def __init__(self, board, boardSize, playerColor, lookAhead):
        self.board = board
        self.boardSize = boardSize
        self.playerColor = playerColor
        self.lookAhead = lookAhead
        self.score = self.staticEvaluation() #in the works
        self.currentPlayer = playerColor
        self.searchLevel = 0


    #My static evaluation function is same as the one discussed in class slides
    #If player color piece reaches the other end of the board +10
    #If opposite of player color pieces reaches the other end of the board -10
    #Else score = number of playerpieces - number of opposite pieces

    def staticEvaluation(self):
        blackPieces = 0
        whitePieces = 0
        firstRow = list(self.board[0]) #maybe broken?
        lastRow = list(self.board[-1]) #maybe broken?
        whiteLost = False
        blackLost = False

    #count the number of white and black pieces on the board
        for row in range(self.boardSize):
            for column in range(self.boardSize):
                if (self.board[row][column] == 'b'):
                    blackPieces += 1
                
                elif (self.board[row][column] == 'w'):
                    whitePieces += 1

                
    #check wins 
        for piece in range (self.boardSize):
            if firstRow[piece] == 'b':  #if a black piece is in top row black wins!
                whiteLost = True    
        for piece in range (self.boardSize):
            if lastRow[piece] == 'w':  #if a white piece is in botom row white wins!
                blackLost = True
        
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if(self.board[i][j] == 'b'):
                    blackPieces += 1
                
                if(self.board[i][j] == 'w'):
                    whitePieces += 1

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
    
class minMaxTree():
    def __init__(self,board):
        self.board = board
        self.parent = None
        self.children = []
        self.level = None # MIN or MAX
    
    def addChild(self, child):
        self.children.append(child)
        child.parent = self
    
    def setMinMax(self):
        if (self.parent):
            if(self.parent.level == 'MAX'):
                self.level = 'MIN'
            else:
                self.level = 'MAX'
        else:
            self.level = 'MAX'

#if the parent is MAX it my search will return node with max score
#if the parent is MIN my search will return node with min score
#parameter is a min max tree isself

def minMaxSearch(head, lookAhead):
    if (head.board.searchLevel < lookAhead - 1):
        if(head.children != []):
            for i in range (len(head.children)):
                if(head.children[i].board.score == -10):
                    break #LOST
                elif(head.children[i].board.score == 10):
                    break #WIN
                minMaxSearch(head.children[i], lookAhead)
        
        if(head.level == 'MAX'):
            maxValue = -10
            maxBoard = head.children[0]
            for i in range (len(head.children)):
                if (head.children[i].board.score > maxValue):
                    maxBoard = head.children[i]
                    maxValue = head.children[i].board.score
            head.board.score = maxBoard.board.score
            head.children.clear()
            return maxBoard
        
        if(head.level == 'MIN'):
            minValue = 10
            minBoard = head.children[0]
            for i in range (len(head.children)):
                if(head.children[i].board.score < minValue):
                    minBoard = head.children[i]
                    minValue = head.children[i].board.score
            head.board.score = minBoard.board.score
            head.children.clear()
            return minBoard

        
def createTree(head):
    if(head.board.lookAhead > 0):
        nextLevel = moveGenerator(head.board) #in progress
        for i in range(len(nextLevel)):
            next = minMaxTree(nextLevel[i])
            head.addChild(next)
            next.setMinMax()
            next.board.lookAhead = (head.board.lookAhead) - 1
            next.board.searchLevel = (head.board.searchLevel) + 1
        for j in range(len(head.children)):
            minMaxTree(head.children[j])
    elif (head.board.lookAhead == 0):
        return
    return head            


#finds the white and black pieces on the coard
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
            elif board[row][column] == 'b':
                blackPieces.append((column,row))
    if(target == 'b'):
        return blackPieces
    elif (target == 'w'):
        return whitePieces
    else:
        return None
            


#MOVEMENT --------------------------------------

def moveWhiteDown(currBoard, column, row):
    board = (currBoard.board).copy()
    # check that position is w
    if(board[row][column] != 'w'):
        return None
    if ((row + 1) >= currBoard.boardSize): #check scope
        return None
    # check under the white piece
    if (board[row + 1][column] == '-'):
        # change current position to '-'
        changeToDash = list(board[row]) 
        changeToDash[column]= '-'
        # 'move' white down
        changeToChar = list(board[row + 1])
        changeToChar[column] = 'w'
        # convert to string
        changeToCharStr = ''.join(changeToChar)
        changeToDashStr = ''.join(changeToDash)
        # replace in board
        board[row] = changeToDashStr
        board[row + 1] = changeToCharStr
    else:
        return None
    return board


def moveWhiteDiagonalLeft(currBoard, column, row):
    board = (currBoard.board).copy()
    # check if curr piece is w
    if (board[row][column] != 'w'):
        return None
    # check if left diagonal is in range
    if((column - 1) < 0) or ((row + 1) >= currBoard.boardSize):
        return None
    # check if left diagonal is b so you can eat it
    if(board[row + 1][column - 1] == 'b'):
        changeToDash = list(board[row])
        changeToDash[column] = '-'
        changeToW = list(board[row + 1])
        changeToW[column - 1] = 'w'
        changeToDashStr = ''.join(changeToDash)
        changeToWStr = ''.join(changeToW)
        board[row] = changeToDashStr
        board[row + 1] = changeToWStr
        return board
    else: 
        return None


def moveWhiteDiagonalRight(currBoard, column, row):
    board = (currBoard.board).copy()
    # check if current piece is w 
    if (board[row][column] != 'w'):
        return None
    # check scope
    if((column + 1) >= currBoard.boardSize) or ((row + 1) >= currBoard.boardSize):
        return None
    # check if right diagonal is b so you can eat it
    if(board[row + 1][column + 1] == 'b'):
        changeToDash = list(board[row])
        changeToDash[column] = '-'
        changeToW = list(board[row + 1])
        changeToW[column + 1] = 'w'
        changeToDashStr = ''.join(changeToDash)
        changeToWStr = ''.join(changeToW)
        board[row] = changeToDashStr
        board[row + 1] = changeToWStr
        return board
    else: 
        return None
    

def moveBlackUp(currBoard, column, row):
    board = (currBoard.board).copy()
    # check that position is b
    if(board[row][column] != 'b'):
        return None
    # check if out of range
    if ((row - 1) < 0):
        return None
    # check if move possible
    if (board[row - 1][column] == '-'):
        # change current position to '-'
        changeToDash = list(board[row]) 
        changeToDash[column]= '-'
        # 'move' white down
        changeToChar = list(board[row - 1])
        changeToChar[column] = 'b'
        # convert to string
        changeToCharStr = ''.join(changeToChar)
        changeToDashStr = ''.join(changeToDash)
        # replace in board
        board[row] = changeToDashStr
        board[row - 1] = changeToCharStr
    else:
        return None
    return board

def moveBlackDiagonalRight(currBoard, column, row):
    board = (currBoard.board).copy()
    # check if curr piece is b
    if (board[row][column] != 'b'):
        return None
    # check if right diagonal is in range
    if ((column + 1) >= currBoard.boardSize) or ((row - 1) < 0):
        return None
    # check if right diagonal is w
    if (board[row - 1][column + 1] == 'w'):
        changeToDash = list(board[row])
        changeToDash[column] = '-'
        changeToW = list(board[row - 1])
        changeToW[column + 1] = 'b'
        changeToDashStr = ''.join(changeToDash)
        changeToWStr = ''.join(changeToW)
        board[row] = changeToDashStr
        board[row - 1] = changeToWStr
        return board
    else:
        return None

def moveBlackDiagonalLeft(currBoard, column, row):
    board = (currBoard.board).copy()
    # check if curr piece is b
    if (board[row][column] != 'b'):
        return None
    # check if left diagonal is in range
    if ((column - 1) < 0) or ((row + 1) < 0):
        return None
    # check if left diagonal is w 
    if(board[row - 1][column - 1] == 'w'):
        changeToDash = list(board[row])
        changeToDash[column] = '-'
        changeToW = list(board[row - 1])
        changeToW[column - 1] = 'b'
        changeToDashStr = ''.join(changeToDash)
        changeToWStr = ''.join(changeToW)
        board[row] = changeToDashStr
        board[row - 1] = changeToWStr
        return board
    else: 
        return None



#stATES-----------------------------------

def whiteStates(white,currBoard):
    possibleStates = []
    for i in range(len(white)):
        down = moveWhiteDown(currBoard, white[i][0], white[i][1])
        right = moveWhiteDiagonalRight(currBoard, white[i][0], white[i][1])
        left = moveWhiteDiagonalRight(currBoard, white[i][0], white[i][1])
        if(down):
            downHex = gameSetup(down,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            downHex.currentPlayer = 'b'
            possibleStates.append(downHex)
        if(right):
            rightHex = gameSetup(right,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            rightHex.currentPlayer = 'b'
            possibleStates.append(rightHex)
        if(left):
            leftHex = gameSetup(left,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            leftHex.currentPlayer = 'b'
            possibleStates.append(leftHex)
    if (possibleStates == []):
        if (currBoard.currentPlayer == currBoard.currentPlayer):
            currBoard.score = -10
        else:
            currBoard.score = 10
    return possibleStates


def blackStates(black,currBoard):
    possibleStates = []
    for i in range(len(black)):
        up = moveBlackUp(currBoard, black[i][0], black[i][1])
        right = moveBlackDiagonalRight(currBoard, black[i][0], black[i][1])
        left = moveBlackDiagonalLeft(currBoard, black[i][0], black[i][1])
        if(up):
            upHex = gameSetup(up,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            upHex.currentPlayer = 'w'
            possibleStates.append(upHex)
        if(right):
            rightHex = gameSetup(right,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            rightHex.currentPlayer = 'w'
            possibleStates.append(rightHex)
        if(left):
            leftHex = gameSetup(left,currBoard.boardSize,currBoard.currentPlayer,currBoard.lookAhead)
            leftHex.currentPlayer = 'w'
            possibleStates.append(leftHex)
    if (possibleStates == []):
        if (currBoard.currentPlayer == currBoard.currentPlayer):
            currBoard.score = -10
        else:
            currBoard.score = 10

def moveGenerator(currGame):
    if (currGame.currentPlayer == 'w'):
        white = findPieces(currGame, 'w')
        possibleStates = whiteStates(white,currGame)
    else:
        black = findPieces(currGame, 'b')
        possibleStates = blackStates(black,currGame)
    return possibleStates 


hexapawn(["www","---","bbb"],3,'w',2)
hexapawn(["www","---","bbb"],3,'b',2)