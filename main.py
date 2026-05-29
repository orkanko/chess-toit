import tkinter as tk
from chess_game import Chess

if __name__ == "__main__":
    # lancer le jeu
    root = tk.Tk()
    root.title("Projet Info S2 CHESS TOIT")
    game = Chess(root)
        
    # Boucle infini pour keep fenêtre
    root.mainloop()