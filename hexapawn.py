#Parminder Singh
#hexapawn

def hexapawn(inputBoard, boardSize, playerColor, lookAhead):
    pass


class gameSetup(object):
    def __init__(self, board, boardSize, playerColor, lookAhead):
        self.board = board
        self.boardSize = boardSize
        self.playerColor = playerColor
        self.lookAhead = lookAhead
        self.score = self.staticEvaluation() #in the works
        self.currentPlayer = playerColor
        self.searchlevel = 0
