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
        self.sudoku.generate_empty_board()
        expected_board = [[0] * 9 for _ in range(9)]
        self.assertEqual(self.sudoku._board, expected_board)
        pass
    
    def test_generate_empty_board_reset(self):
        self.sudoku._board[0][0] = 1
        self.sudoku.generate_empty_board()  
        expected_board = [[0] * 9 for _ in range(9)]
        self.assertEqual(self.sudoku._board, expected_board)

    def test_is_valid(self):
        self.assertTrue(self.sudoku.is_valid(0, 2, 1), "Le placement devrait être valide.")

    def test_is_valid_invalid_row(self):
        self.assertFalse(self.sudoku.is_valid(0, 2, 5), "Le placement devrait être invalide à cause de la ligne.")

    def test_is_valid_invalid_column(self):
        self.assertFalse(self.sudoku.is_valid(2, 0, 6), "Le placement devrait être invalide à cause de la colonne.")

    def test_is_valid_invalid_block(self):
        self.assertFalse(self.sudoku.is_valid(1, 2, 3), "Le placement devrait être invalide à cause du bloc.")
    
    def test_find_empty_empty_board(self):
        self.sudoku.generate_empty_board()  
        expected_position = (0, 0)  
        self.assertEqual(self.sudoku.find_empty(), expected_position, "La première case vide devrait être en position (0, 0)")

    def test_find_empty_empty_spaces(self):
        self.sudoku.generate_empty_board()  
        for i in range(8):
            for j in range(9):
                self.sudoku._board[i][j] = i+j+1
        expected = (8, 0)
        self.assertEqual(self.sudoku.find_empty(), expected)

    def test_find_empty_full_board(self):
        self.sudoku._board = [[1] * 9 for _ in range(9)]  
        self.assertIsNone(self.sudoku.find_empty(), "Aucune case vide ne devrait être trouvée sur un plateau complètement rempli")
          
    def test_is_valid(self):
        self.sudoku.generate_empty_board()
        self.assertTrue(self.sudoku.is_valid(0, 0, 1)) 
        self.sudoku._board[0][1] = 1
        self.assertFalse(self.sudoku.is_valid(0, 0, 1))  
        self.sudoku._board[1][0] = 2
        self.assertFalse(self.sudoku.is_valid(0, 0, 2))  

    def test_find_empty(self):
        self.sudoku.generate_empty_board()
        self.assertIsNotNone(self.sudoku.find_empty())
        self.sudoku._board = [[1]*9 for _ in range(9)]
        self.assertIsNone(self.sudoku.find_empty())

    def test_solve_sudoku(self):
        self.sudoku.generate_empty_board()
        self.assertTrue(self.sudoku.solve_sudoku())
        self.assertIsNone(self.sudoku.find_empty())

    def test_solve_sudoku_success(self):
        result = self.sudoku.solve_sudoku()
        self.assertTrue(result, "Le Sudoku doit être résolu.")
        self.assertIsNone(self.sudoku.find_empty(), "Il ne devrait y avoir aucune cellule vide après la résolution.")

    def test_solve_sudoku_fail(self):
        self.sudoku._board[0][2] = 3  
        result = self.sudoku.solve_sudoku()
        self.assertFalse(result, "Le Sudoku ne doit pas être résolu à cause d'un conflit.")
        
    def test_generate_view_board_creates_solvable_sudoku(self):
        for difficulty in ["Easy", "Intermediate", "Advanced"]:
            with self.subTest(difficulty=difficulty):
                self.sudoku.generate_view_board(difficulty)
                solvable = self.sudoku.solve_sudoku()
                self.assertTrue(solvable, f"Le plateau généré avec la difficulté '{difficulty}' devrait être résolvable.")

    def test_generate_view_board_difficulty(self):
        self.sudoku.generate_view_board("Advanced")
        advanced_filled = sum(row.count(0) for row in self.sudoku._board)
        self.sudoku.generate_view_board("Easy")
        easy_filled = sum(row.count(0) for row in self.sudoku._board)
        self.assertTrue(easy_filled < advanced_filled, "Le mode 'Facile' devrait avoir moins de cases vides que le mode 'Avancé'.")

    def test_Indice_empty_cell(self):
        self.sudoku.generate_empty_board()
        self.sudoku._board[0][0] = 5 
        expected_indices = [1, 2, 3, 4, 6, 7, 8, 9]  
        indices = self.sudoku.Indice(0, 1)  
        self.assertEqual(sorted(indices), expected_indices, "Devrait retourner les indices valides.")
                         
    def test_Indice_empty_cell_valid_indices(self):
        self.sudoku._board = [
            [0, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0, 0, 0, 5, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        expected_indices = [3, 4, 5, 6, 7, 8, 9]
        indices = self.sudoku.Indice(0, 0)
        self.assertEqual(sorted(indices), expected_indices, "Devrait retourner les indices valides.")

    def test_Board_Complete_full_board(self):
        self.sudoku._board = [[1] * 9 for _ in range(9)]  
        self.assertTrue(self.sudoku.Board_Complete(), "Devrait retourner True pour un plateau rempli.")
    
    def test_Board_Complete_with_empty_cell(self):
        self.sudoku.generate_empty_board() 
        self.sudoku._board[0][0] = 1  
        self.assertFalse(self.sudoku.Board_Complete(), "Devrait retourner False si au moins une case est vide.")



if __name__ == '__main__':
    unittest.main()
