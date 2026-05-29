from position import Position
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        # On crée une grille 8x8 de none
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.initBoard()

    def getPiece(self, position):
        # si pièce, on prends
        return self.grid[position.row][position.column]

    def initBoard(self):
        for i in range(8):         # Place pions
            self.grid[1][i] = Pawn(Position(i, 1), 0) # La ligne des blancs
            self.grid[6][i] = Pawn(Position(i, 6), 1) # La ligne des noirs
        
        layout = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]         # cree ordre pieces pricipalesr
        
        for i in range(8): #Place pieces pricipales
            self.grid[0][i] = layout[i](Position(i, 0), 0)
            self.grid[7][i] = layout[i](Position(i, 7), 1)