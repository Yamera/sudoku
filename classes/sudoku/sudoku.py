import sys
import random
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from classes.difficulty.difficulty import Difficulty

__name__ = "sudoku"
__author__ = "Yasmine "
__version__ = 1.0


"""
	Classe Sudoku.
	> Une interface pour votre jeu Sudoku.
"""


class Sudoku:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._board = [[0 for _ in range(9)] for _ in range(9)]
            instance.chances = 3
            instance.Etat_Du_jeu = "En partie"
            cls._instance = instance
        return cls._instance

    def generate_empty_board(self):
        """
        Réinitialise le plateau à un état entièrement vide.
        """
        self._board = [[0] * 9 for _ in range(9)]

    def is_valid(self, row, col, num):
        for i in range(9):
            if self._board[row][i] == num:
                return False
        for i in range(9):
            if self._board[i][col] == num:
                return False
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self._board[startRow + i][startCol + j] == num:
                    return False
        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self._board[i][j] == 0:
                    return (i, j)
        return None

    def solve_sudoku(self):
        find = self.find_empty()
        if not find:
            return True  
        else:
            row, col = find

        nums = list(range(1, 10))  
        random.shuffle(nums)  

        for num in nums:  
            if self.is_valid(row, col, num):  
                self._board[row][col] = num
                if self.solve_sudoku():  
                    return True
                self._board[row][col] = 0  

        return False

    def generate_view_board(self, difficulty="Easy"):
        """
        Génère un plateau de jeu selon la difficulté spécifiée.
        """
        self.generate_empty_board()
        self.solve_sudoku()
        if difficulty == "Easy":
            CaseRemplie = random.randint(40, 49)  
        elif difficulty == "Intermediate":
            CaseRemplie = random.randint(30, 39)
        elif difficulty == "Advanced":
            CaseRemplie = random.randint(20, 29)
        else:
            raise ValueError("Difficulté non valide")

        CaseVide = 81 - CaseRemplie
        while CaseVide > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self._board[row][col] != 0:  
                self._board[row][col] = 0
                CaseVide -= 1
    
    def Indice(self, row, col): #Genere indices
        indices = [num for num in range(1, 10) if self.is_valid(row, col, num)]
        return indices

    def Board_Complete(self):
        for row in self._board:
            for cell in row:
                if cell == 0: 
                    return False 
        return True       



sudoku_game = Sudoku()

