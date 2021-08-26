#Parminder Singh
#hexapawn

def hexapawn(inputBoard, boardSize, playerColor, lookAhead):
    startGame = gameSetup(inputBoard, boardSize, playerColor, lookAhead)



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
    
    for i in range(self.size):
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
        self.level = None
    
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
                if(head.children[i].game.score == -10):
                    break #LOST
                elif(head.children[i].game.score == 10):
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
            for in range (len(head.children)):
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
    elif (head.board.searchAhead == 0):
        return
    return head            
            
def findPieces(currBoard, target):
    size = currBoard.size
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
            



#MOVEMENT ---------------------------------------




#stATES-----------------------------------