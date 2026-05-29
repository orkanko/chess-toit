from position import Position

class Piece:
    # La classe mere pour toutes les pièces,
    def __init__(self, position, color):
        self.position = position
        self.color = color # 0 pour les blancs, 1 pour les noirs

    def isValidMove(self, newPosition, board):
        # A verfifier plus tard pr l'instant tt est valide
        return True

# TIAGO
class Knight(Piece):
    def __str__(self): return "♘" if self.color == 0 else "♞"
    
    def isValidMove(self, newPosition, board):
        # en L
        dx = abs(newPosition.column - self.position.column)
        dy = abs(newPosition.row - self.position.row)
        
        # Si ça fait 2 d'un côté et 1 de l'autre
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)


# ILAN
class Pawn(Piece):
    def __str__(self): return "♙" if self.color == 0 else "♟"
    
    def isValidMove(self, newPosition, board):
        # tout droit
        direction = 1 if self.color == 0 else -1
        dy = newPosition.row - self.position.row
        dx = newPosition.column - self.position.column
        
        return dx == 0 and dy == direction

# ORTHIA
class Bishop(Piece):
    def __str__(self): return "♗" if self.color == 0 else "♝"
    
    def isValidMove(self, newPosition, board):
        #ull diagonale
        dx = abs(newPosition.column - self.position.column)
        dy = abs(newPosition.row - self.position.row)
        
        return dx == dy and dx > 0

# THIBAULT
class Rook(Piece):
    def __str__(self): return "♖" if self.color == 0 else "♜"
    
    def isValidMove(self, newPosition, board):
        # tout droit en ligne on colonne
        dx = abs(newPosition.column - self.position.column)
        dy = abs(newPosition.row - self.position.row)
        
        # x bouge pas OU  y bouge pas
        return (dx == 0 and dy > 0) or (dy == 0 and dx > 0)

class Queen(Piece):
    def __str__(self): return "♕" if self.color == 0 else "♛"
    def isValidMove(self, newPosition, board): 
        # a voir plus tard
        return True

class King(Piece):
    def __str__(self): return "♔" if self.color == 0 else "♚"
    def isValidMove(self, newPosition, board): 
        # a voir plus tard
        return True