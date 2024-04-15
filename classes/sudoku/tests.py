import unittest
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from classes.sudoku.sudoku import Sudoku



# __name__ = "tests"
__author__ = "<votre nom>"
__version__ = 1.0


"""
	Tests unitaires pour Sudoku.
	> Testez chacune de vos méthodes de la classe Sudoku.
	> Deux cas de tests par méthode, voir l'énoncé.
"""


class TestSudoku(unittest.TestCase):
    def setUp(self) -> None:
        """
        TODO: Initialiser les ressources avant chaque test.
        """
        self.sudoku = Sudoku()
        self.sudoku._board = [
            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0], 
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0] 
        ]

    def test_generate_empty_board(self):
        """
        TODO: Tester si le tableau vide est généré correctement.
        """
        self.sudoku.generate_empty_board()
        expected_board = [[0] * 9 for _ in range(9)]
        self.assertEqual(self.sudoku._board, expected_board)
        pass
    
    def test_generate_empty_board_reset(self):
        self.sudoku._board[0][0] = 1
        self.sudoku.generate_empty_board()  
        expected_board = [[0] * 9 for _ in range(9)]
        self.assertEqual(self.sudoku._board, expected_board)

    def test_is_valid_placement_valid(self):
        # Teste un placement valide qui ne viole aucune règle
        self.assertTrue(self.sudoku.is_valid(0, 2, 1), "Le placement devrait être valide.")

    def test_is_valid_placement_invalid_row(self):
        # Teste un placement invalide en raison d'une répétition dans la même ligne
        self.assertFalse(self.sudoku.is_valid(0, 2, 5), "Le placement devrait être invalide à cause de la ligne.")

    def test_is_valid_placement_invalid_column(self):
        # Teste un placement invalide en raison d'une répétition dans la même colonne
        self.assertFalse(self.sudoku.is_valid(2, 0, 6), "Le placement devrait être invalide à cause de la colonne.")

    def test_is_valid_placement_invalid_block(self):
        # Teste un placement invalide en raison d'une répétition dans le même bloc
        self.assertFalse(self.sudoku.is_valid(1, 2, 3), "Le placement devrait être invalide à cause du bloc.")
    
    def test_find_empty_on_empty_board(self):
        self.sudoku.generate_empty_board()  # Assurez-vous que le plateau est vide
        expected_position = (0, 0)  # La première position doit être vide
        self.assertEqual(self.sudoku.find_empty(), expected_position, "La première case vide devrait être en position (0, 0)")

    def test_complete_board(self):
        """
        TODO: Tester si le tableau est complété correctement.
        """
        self.sudoku.generate_view_board("Facile")
        facile_count = sum(row.count(0) for row in self.sudoku._board())
        self.assertTrue(36 <= 81 - facile_count <= 41)

        self.sudoku.generate_view_board("Intermediaire")
        intermediaire_count = sum(row.count(0) for row in self.sudoku._board())
        self.assertTrue(32 <= 81 - intermediaire_count <= 35)
        pass

    def test_find_empty_on_full_board(self):
        self.sudoku._board = [[1] * 9 for _ in range(9)]
        self.assertIsNone(self.sudoku.find_empty(), "Aucune case vide ne devrait être trouvée sur un plateau complètement rempli")

    def test_generate_view_board(self):
        """
        TODO: Tester si le plateau de jeu pour l'utilisateur est généré correctement.
        """
        for difficulty, expected_range in [("Facile", (36, 41)), ("Intermediaire", (32, 35)), ("Avancé", (28, 31))]:
            with self.subTest(difficulty=difficulty):
                self.sudoku.generate_view_board(difficulty)
                filled_cells = sum(1 for row in self.sudoku.get_board() for cell in row if cell != 0)
                self.assertIn(filled_cells, range(expected_range[0], expected_range[1] + 1))
                              
    def test_is_valid(self):
        """Teste la méthode is_valid pour des cas valides et invalides."""
        self.sudoku.generate_empty_board()
        self.assertTrue(self.sudoku.is_valid(0, 0, 1))  # Valide
        self.sudoku._board[0][1] = 1
        self.assertFalse(self.sudoku.is_valid(0, 0, 1))  # Invalide, même ligne
        self.sudoku._board[1][0] = 2
        self.assertFalse(self.sudoku.is_valid(0, 0, 2))  # Invalide, même colonne

    def test_find_empty(self):
        """Teste si find_empty retourne correctement une case vide ou None."""
        self.sudoku.generate_empty_board()
        self.assertIsNotNone(self.sudoku.find_empty())
        self.sudoku._board = [[1]*9 for _ in range(9)]
        self.assertIsNone(self.sudoku.find_empty())

    def test_solve_sudoku(self):
        """Teste si le Sudoku est résolu correctement."""
        self.sudoku.generate_empty_board()
        self.assertTrue(self.sudoku.solve_sudoku())
        # Vérifie qu'il n'y a plus de cases vides
        self.assertIsNone(self.sudoku.find_empty())
    def test_generate_view_board_creates_solvable_puzzle(self):
        """
        Teste si generate_view_board génère un plateau jouable avec la difficulté spécifiée.
        """
        for difficulty in ["Easy", "Intermediate", "Advanced"]:
            with self.subTest(difficulty=difficulty):
                self.sudoku.generate_view_board(difficulty)
                solvable = self.sudoku.solve_sudoku()
                self.assertTrue(solvable, f"Le plateau généré avec la difficulté '{difficulty}' devrait être résolvable.")

    def test_generate_view_board_difficulty_impact(self):
        """
        Vérifie que le nombre de cases pré-remplies varie selon la difficulté.
        """
        self.sudoku.generate_view_board("Advanced")
        advanced_filled = sum(row.count(0) for row in self.sudoku._board)
        self.sudoku.generate_view_board("Easy")
        easy_filled = sum(row.count(0) for row in self.sudoku._board)
        self.assertTrue(easy_filled < advanced_filled, "Le mode 'Facile' devrait avoir moins de cases vides que le mode 'Avancé'.")
    def test_sol_valide_with_invalid_solution(self):
        """Teste la validation d'une solution invalide."""
        self.sudoku._board[0][0] = self.sudoku._board[1][0]  # Crée un doublon intentionnel
        self.assertFalse(self.sudoku.sol_valide(), "La méthode devrait retourner False pour une solution invalide.")

    def test_sol_valide_with_valid_solution(self):
        """Teste la validation d'une solution valide."""
        self.sudoku.solve_sudoku()  # Génère une solution valide
        self.assertTrue(self.sudoku.sol_valide(), "La méthode devrait retourner True pour une solution valide.")

    def test_case_vide_with_full_board(self): #CaseVide
        """Teste la recherche de cases vides sur un plateau complet."""
        self.sudoku.solve_sudoku()  # Remplit le plateau
        self.assertEqual(len(self.sudoku.CaseVide()), 0, "Il ne devrait y avoir aucune case vide sur un plateau complet.")

    def test_case_vide_with_empty_board(self): #CaseVide
        """Teste la recherche de cases vides sur un plateau vide."""
        self.sudoku.generate_empty_board()  # Vide le plateau
        self.assertEqual(len(self.sudoku.CaseVide()), 81, "Il devrait y avoir 81 cases vides sur un plateau vide.")
    
    def test_indice_with_full_board(self): #Indice
        """Teste la génération d'indices sur un plateau complet."""
        self.sudoku.solve_sudoku()  # Remplit le plateau
        self.assertIsNone(self.sudoku.Indice(), "Il ne devrait y avoir aucun indice disponible sur un plateau complet.")

    def test_indice_with_empty_board(self): #Indice
        """Teste la génération d'indices sur un plateau vide."""
        self.sudoku.generate_empty_board()  # Vide le plateau
        indice = self.sudoku.Indice()
        self.assertIsNotNone(indice, "Un indice devrait être disponible sur un plateau vide.")

    def test_indice_dispo_decreases_chances(self): #IndiceDispo
        """Teste si Indice_Dispo diminue le nombre de chances."""
        initial_chances = self.sudoku.chances
        self.sudoku.Indice_Dispo()  # Appelle la méthode une fois
        self.assertEqual(self.sudoku.chances, initial_chances - 1, "Le nombre de chances devrait diminuer de 1.")

    def test_etat_du_jeu_win(self): #IndiceDispo
        """Teste si EtatDuJeu renvoie 'gagné' pour un plateau complété correctement."""
        self.sudoku.solve_sudoku()
        self.sudoku.EtatDuJeu()
        self.assertEqual(self.sudoku.Etat_Du_jeu, "gagné", "L'état du jeu devrait être 'gagné' pour un plateau complété correctement.")

if __name__ == '__main__':
    unittest.main()
