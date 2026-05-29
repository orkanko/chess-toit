# =============================================================
#  test_pieces.py  — Tests unitaires (framework unittest)
# =============================================================

import unittest
import os
import sys

# ── FAUX MODULE PYGAME (MOCKING) POUR LES TESTS CONTENEURS ──
# Cette structure simule Pygame pour exécuter les tests dans la console 
# sans ouvrir de fenêtre graphique et sans planter sur les imports de pièces.

class PygameMock:
    SRCALPHA = 0
    
    def Surface(self, *args, **kwargs): 
        return None
        
    class transform:
        @staticmethod
        def smoothscale(*args): return None
        @staticmethod
        def scale(*args): return None
        
    class image:
        @staticmethod
        def load(*args):
            class FakeImage:
                def convert(self): return None
                def convert_alpha(self): return None
            return FakeImage()
            
    class font:
        @staticmethod
        def SysFont(*args, **kwargs):
            class FakeFont:
                def render(self, *args, **kwargs): return None
                def size(self, *args): return (0, 0)
            return FakeFont()

# On injecte manuellement notre faux module dans le registre système global de Python
sys.modules["pygame"] = PygameMock()


# ── IMPORTS DU PROJET ─────────────────────────────────────────
from position  import Position
from pieces    import King, Queen, Bishop, Knight, Rook, Pawn, WHITE, BLACK


# ── SIMULATION DE PLATEAU (MOCK BOARD) POUR LES TESTS ────────
class MockBoard:
    """Plateau ultra-simplifié contenant uniquement une liste de pièces."""
    
    def __init__(self, pieces=None):
        if pieces is None:
            self.pieces = []
        else:
            self.pieces = list(pieces)

    def getPiece(self, pos):
        """Recherche si une pièce vivante occupe la position demandée."""
        for piece in self.pieces:
            if not piece.isCaptured:
                if piece.position == pos:
                    return piece
        return None

    def getActivePieces(self, color=None):
        """Retourne la liste des pièces encore en jeu (filtrable par couleur)."""
        active_list = []
        for piece in self.pieces:
            if not piece.isCaptured:
                if color is None or piece.color == color:
                    active_list.append(piece)
        return active_list

    def removePiece(self, piece):
        """Marque une pièce comme capturée et la retire du plateau."""
        piece.isCaptured = True
        self.pieces.remove(piece)

    def getPieceImage(self, key): return None
    def to_dict(self): return {"pieces": []}
    def from_dict(self, data): pass


def pos(col, row):
    """Raccourci utilitaire pour instancier rapidement une Position."""
    return Position(col, row)


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — POSITION
# ═════════════════════════════════════════════════════════════
class TestPosition(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(pos("e", 1)), "e1")
        self.assertEqual(str(pos("A", 8)), "a8")

    def test_eq(self):
        self.assertEqual(pos("e", 1), pos("e", 1))
        self.assertNotEqual(pos("e", 1), pos("e", 2))

    def test_col_index(self):
        self.assertEqual(pos("a", 1).col_index, 0)
        self.assertEqual(pos("h", 1).col_index, 7)

    def test_invalid_column(self):
        """Vérifie que la validation lève bien une erreur sur une colonne erronée."""
        with self.assertRaises(ValueError):
            p = pos("a", 1)
            p.column = "z"


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — PION (Pawn)
# ═════════════════════════════════════════════════════════════
class TestPawn(unittest.TestCase):

    def test_avance_une_case(self):
        pawn = Pawn(pos("e", 2), WHITE)
        board = MockBoard([pawn])
        self.assertTrue(pawn.isValidMove(pos("e", 3), board))

    def test_avance_deux_cases_depart(self):
        pawn = Pawn(pos("e", 2), WHITE)
        board = MockBoard([pawn])
        self.assertTrue(pawn.isValidMove(pos("e", 4), board))

    def test_pas_deux_cases_si_deja_bouge(self):
        pawn = Pawn(pos("e", 3), WHITE)  # Pas sur sa ligne de départ (ligne 2)
        board = MockBoard([pawn])
        self.assertFalse(pawn.isValidMove(pos("e", 5), board))

    def test_bloque_par_piece(self):
        pawn = Pawn(pos("e", 2), WHITE)
        blocker = Pawn(pos("e", 3), BLACK)
        board = MockBoard([pawn, blocker])
        self.assertFalse(pawn.isValidMove(pos("e", 3), board))

    def test_capture_diagonale(self):
        pawn = Pawn(pos("e", 4), WHITE)
        target = Pawn(pos("f", 5), BLACK)
        board = MockBoard([pawn, target])
        self.assertTrue(pawn.isValidMove(pos("f", 5), board))


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — TOUR (Rook)
# ═════════════════════════════════════════════════════════════
class TestRook(unittest.TestCase):

    def test_deplacement_horizontal(self):
        rook = Rook(pos("a", 1), WHITE)
        board = MockBoard([rook])
        self.assertTrue(rook.isValidMove(pos("h", 1), board))

    def test_bloquee_par_allie(self):
        rook = Rook(pos("a", 1), WHITE)
        blocker = Rook(pos("d", 1), WHITE)
        board = MockBoard([rook, blocker])
        self.assertFalse(rook.isValidMove(pos("h", 1), board))


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — FOU (Bishop)
# ═════════════════════════════════════════════════════════════
class TestBishop(unittest.TestCase):

    def test_deplacement_diagonal(self):
        bishop = Bishop(pos("c", 1), WHITE)
        board = MockBoard([bishop])
        self.assertTrue(bishop.isValidMove(pos("f", 4), board))


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — CAVALIER (Knight)
# ═════════════════════════════════════════════════════════════
class TestKnight(unittest.TestCase):

    def test_mouvement_en_L(self):
        knight = Knight(pos("b", 1), WHITE)
        board = MockBoard([knight])
        self.assertTrue(knight.isValidMove(pos("c", 3), board))

    def test_saute_par_dessus(self):
        knight = Knight(pos("b", 1), WHITE)
        blocker = Pawn(pos("b", 2), WHITE)
        board = MockBoard([knight, blocker])
        self.assertTrue(knight.isValidMove(pos("c", 3), board))  # Doit passer par-dessus !


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — REINE (Queen)
# ═════════════════════════════════════════════════════════════
class TestQueen(unittest.TestCase):

    def test_diagonale(self):
        queen = Queen(pos("d", 4), WHITE)
        board = MockBoard([queen])
        self.assertTrue(queen.isValidMove(pos("g", 7), board))


# ═════════════════════════════════════════════════════════════
#  TESTS COMPOSANT — ROI (King)
# ═════════════════════════════════════════════════════════════
class TestKing(unittest.TestCase):

    def test_une_case_autour(self):
        king = King(pos("e", 1), WHITE)
        board = MockBoard([king])
        # On teste manuellement quelques cases adjacentes valides
        self.assertTrue(king.isValidMove(pos("e", 2), board))
        self.assertTrue(king.isValidMove(pos("d", 2), board))

    def test_plus_dune_case_invalide(self):
        king = King(pos("e", 1), WHITE)
        board = MockBoard([king])
        self.assertFalse(king.isValidMove(pos("e", 3), board))


# ═════════════════════════════════════════════════════════════
#  TESTS LOGIQUES GLOBALES — ÉCHEC ET MAT
# ═════════════════════════════════════════════════════════════
class TestCheckLogic(unittest.TestCase):

    def _make_chess(self, pieces):
        """Instancie manuellement un moteur de jeu injecté de pièces de simulation."""
        from chess_game import Chess
        from player     import Player

        # Instanciation brute de l'objet sans exécuter son __init__ graphique
        game = Chess.__new__(Chess)
        game.board = MockBoard(pieces)
        game._status_msg = ""
        game._game_over = False
        game._selected = None
        game._valid_moves = []

        player_w = Player(WHITE)
        player_w.name = "Blanc"
        player_b = Player(BLACK)
        player_b.name = "Noir"
        
        game.players = [player_w, player_b]
        game.currentPlayer = player_w
        return game

    def test_isCheck_vrai(self):
        """Une tour noire vise directement le roi blanc en ligne droite."""
        king = King(pos("e", 1), WHITE)
        attacker = Rook(pos("e", 8), BLACK)
        game = self._make_chess([king, attacker])
        
        self.assertTrue(game.isCheck(WHITE))

    def test_isMoveSafe(self):
        """Un coup cloué qui mettrait son propre roi en échec doit être intercepté."""
        king = King(pos("e", 1), WHITE)
        shield = Rook(pos("e", 4), WHITE)   # Bloque l'attaque ennemie
        attacker = Rook(pos("e", 8), BLACK)  # Vise le roi en ligne droite
        
        game = self._make_chess([king, shield, attacker])
        
        # Déplacer la tour blanche sur le côté démasquerait l'attaque -> Non sécurisé !
        self.assertFalse(game.isMoveSafe(shield, pos("a", 4)))

    def test_checkmate(self):
        """Simulation simplifiée d'une situation d'Échec et Mat étanche."""
        king_w = King(pos("a", 1), WHITE)
        rook_b1 = Rook(pos("h", 1), BLACK)  # Verrouille toute la ligne 1 (où se trouve le Roi)
        rook_b2 = Rook(pos("h", 2), BLACK)  # Verrouille toute la ligne 2 (toutes les cases d'esquive)
        
        game = self._make_chess([king_w, rook_b1, rook_b2])
        
        # Le roi est attaqué et n'a aucune échappatoire possible -> Mat !
        self.assertTrue(game.isCheckMate())


if __name__ == "__main__":
    unittest.main(verbosity=2)