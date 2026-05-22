from abs import ABC, abstractmethod

class Position:
    def __init__(self,row:int,column:str):
        self.row = row
        self.column = column

    def __str__(self):
        return f"{self.column}{self.row}"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Piece(ABC):
    def __init__(self,pos,color):
        self.isCaptured = False
        self.position = Position(pos)
        self.color = color

    @abstractmethod
    def isValidMove(self,newPosition,board):
        pass

class King(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "K"

class Queen(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "Q"

class Bishop(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "B"

class Knight(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "N"

class Rook(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "R"

class Pawn(Piece):
    def isValidMove(self,newPosition,board):
        pass

    def __str__(self):
        return "P"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Board:
    def getPosition(piece):
        if not piece.isCaptured:
            return piece.position

    def getPiece(position):
        pass

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

class Player:
    def __init__(self,color):
        self.name = ""
        self.color = color
