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

    def test_is_valid_placement_valid(self):
        self.assertTrue(self.sudoku.is_valid(0, 2, 1), "Le placement devrait être valide.")

    def test_is_valid_placement_invalid_row(self):
        self.assertFalse(self.sudoku.is_valid(0, 2, 5), "Le placement devrait être invalide à cause de la ligne.")

    def test_is_valid_placement_invalid_column(self):
        self.assertFalse(self.sudoku.is_valid(2, 0, 6), "Le placement devrait être invalide à cause de la colonne.")

    def test_is_valid_placement_invalid_block(self):
        self.assertFalse(self.sudoku.is_valid(1, 2, 3), "Le placement devrait être invalide à cause du bloc.")
    
    def test_find_empty_on_empty_board(self):
        self.sudoku.generate_empty_board()  
        expected_position = (0, 0)  
        self.assertEqual(self.sudoku.find_empty(), expected_position, "La première case vide devrait être en position (0, 0)")

    def test_find_empty_with_empty_spaces(self):
        self.sudoku.generate_empty_board()  
        for i in range(8):
            for j in range(9):
                self.sudoku._board[i][j] = i+j+1
        expected = (8, 0)
        self.assertEqual(self.sudoku.find_empty(), expected)

    def test_find_empty_on_full_board(self):
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
        
    def test_generate_view_board_creates_solvable_puzzle(self):
        for difficulty in ["Easy", "Intermediate", "Advanced"]:
            with self.subTest(difficulty=difficulty):
                self.sudoku.generate_view_board(difficulty)
                solvable = self.sudoku.solve_sudoku()
                self.assertTrue(solvable, f"Le plateau généré avec la difficulté '{difficulty}' devrait être résolvable.")

    def test_generate_view_board_difficulty_impact(self):
        self.sudoku.generate_view_board("Advanced")
        advanced_filled = sum(row.count(0) for row in self.sudoku._board)
        self.sudoku.generate_view_board("Easy")
        easy_filled = sum(row.count(0) for row in self.sudoku._board)
        self.assertTrue(easy_filled < advanced_filled, "Le mode 'Facile' devrait avoir moins de cases vides que le mode 'Avancé'.")

    def test_sol_valide_with_invalid_solution(self):
        self.sudoku._board[0][0] = self.sudoku._board[1][0]  
        self.assertFalse(self.sudoku.sol_valide(), "Devrait retourner False pour une solution invalide.")

    def test_sol_valide_with_valid_solution(self):
        self.sudoku.solve_sudoku()  
        self.assertTrue(self.sudoku.sol_valide(), "Devrait retourner True pour une solution valide.")

    def test_Indice_with_empty_cell(self):
        self.sudoku.generate_empty_board()
        self.sudoku._board[0][0] = 5 
        expected_indices = [1, 2, 3, 4, 6, 7, 8, 9]  
        indices = self.sudoku.Indice(0, 1)  
        self.assertEqual(sorted(indices), expected_indices, "Devrait retourner les indices valides.")
                         
    def test_Indice_with_empty_cell_provides_valid_indices(self):
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

    def test_Board_Complete_with_full_board(self):
        self.sudoku._board = [[1] * 9 for _ in range(9)]  
        self.assertTrue(self.sudoku.Board_Complete(), "Devrait retourner True pour un plateau rempli.")
    
    def test_Board_Complete_with_at_least_one_empty_cell(self):
        self.sudoku.generate_empty_board() 
        self.sudoku._board[0][0] = 1  
        self.assertFalse(self.sudoku.Board_Complete(), "Devrait retourner False si au moins une case est vide.")



if __name__ == '__main__':
    unittest.main()
