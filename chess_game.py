import tkinter as tk
from board import Board
from position import Position
from player import Player

class Chess:
    def __init__(self, root):
        self.root = root # La fenêtre principale de l'appli
        self.board = Board()
        self.players = [Player("P1", 0), Player("P2", 1)] # Les deux personnes en VS
        self.currentPlayer = self.players[0] # Blanc starts
        
        # La grille des boutons pour cliquer dessus dans l'interface
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_pos = None # Rien est clique a la base
        
        self.displayBoard()

    def displayBoard(self):
        # On genere la boad
        for row in range(8):
            for col in range(8):
                # couleur blanc casse et vert
                bg_color = "#eeeed2" if (row + col) % 2 == 0 else "#769656"
                
                # On fait un boutton aui sert de case
                btn = tk.Button(self.root, text="", font=("Arial", 32), bg=bg_color, 
                                activebackground="#fc5a1a",  #couleur des boutton on hovered
                                command=lambda r=row, c=col: self.play_turn(r, c))
                btn.grid(row=row, column=col, sticky="nsew")
                
                self.buttons[row][col] = btn
                
        self.update_ui()

    def update_ui(self):
        #  icones des pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                self.buttons[row][col].config(text=str(piece) if piece else "")

    def play_turn(self, row, col):
        clicked_pos = Position(col, row)
        
        # si peice pas choisie
        if not self.selected_pos:
            if self.board.getPiece(clicked_pos): # on verifie quy a une piece sur le boutton clicker
                self.selected_pos = clicked_pos
                self.buttons[row][col].config(bg="#fc5a1a") # Oboutton selectioner en rouge
                
        # Si piece choisie
        else:
            piece = self.board.getPiece(self.selected_pos)
            
            # si le mouve qu'on essaie de faire est bon par rapport a ce qu;on a dit 
            if piece and piece.isValidMove(clicked_pos, self.board):
                # change la positin de la piece
                self.board.grid[row][col] = piece
                self.board.grid[self.selected_pos.row][self.selected_pos.column] = None
                piece.position = clicked_pos
            
            # refresj
            self.selected_pos = None
            self.displayBoard() 
            self.update_ui()