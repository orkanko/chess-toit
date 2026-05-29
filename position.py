class Position:
    # En gros ça c'est juste pour dire où est la pièce sur le plateau
    def __init__(self, column, row):
        self.column = column # La colonne, genre l'axe x
        self.row = row       # La ligne, genre l'axe y