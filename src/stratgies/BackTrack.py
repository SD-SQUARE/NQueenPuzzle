import time
import random
from PuzzleStratgy import PuzzleStratgy
from utils.validations import NValidation


class BackTrack(PuzzleStratgy):

    def __init__(self):
        self.solutions = []
        self.solution_times = []
        self.board = []
        self.start_index_row = -1
        self.start_index_column = -1
        self.total_time = 0

    # ------------------------------------------
    # Check if placing a queen is safe
    # ------------------------------------------
    def is_safe(self, row, col, n):
        # Check column
        for i in range(row):
            if self.board[i][col] == 1:
                return False

        # Check upper-left diagonal
        i, j = row, col
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        # Check upper-right diagonal
        i, j = row, col
        while i >= 0 and j < n:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j += 1

        return True

    # ------------------------------------------
    # Backtracking algorithm
    # ------------------------------------------
    def solve_nqueens(self, row, n, start_time):
        if row == n:
            solution_time = time.time() - start_time

            solution = [
                "".join("Q" if cell == 1 else "." for cell in r)
                for r in self.board
            ]

            self.solutions.append(solution)
            self.solution_times.append(solution_time)
            return

        for col in range(n):
            if self.is_safe(row, col, n):
                self.board[row][col] = 1
                self.solve_nqueens(row + 1, n, start_time)
                self.board[row][col] = 0  

    # ------------------------------------------------
    # TODO: implement solve() using backtracking
    # ------------------------------------------------
    def solve(self, N=4):
        NValidation.validate(N)

        # Initialize board
        self.board = [[0] * N for _ in range(N)]
        self.solutions = []
        self.solution_times = []

        # Random start index
        self.start_index_row = 0
        self.start_index_column = random.randint(0, N - 1)
        self.board[0][self.start_index_column] = 1

        start_time = time.time()
        self.solve_nqueens(1, N, start_time)
        self.total_time = time.time() - start_time

    def generateReport(self, N=4):
        if N < 4:
            raise ValueError("N must be >= 4")

        report = "\n" + "="*40 + "\n"
        report += f"      N-Queens Report (N = {N})\n"
        report += "="*40 + "\n"
        report += f"Random Start Index: (row={self.start_index_row}, col={self.start_index_column})\n"
        report += f"Total number of solutions: {len(self.solutions)}\n"
        report += f"Total execution time: {self.total_time:.6f} seconds\n\n"

        for i, (sol, t) in enumerate(zip(self.solutions, self.solution_times), 1):
            report += f"Solution {i} (found at {t:.6f} seconds):\n"
            report += "\n".join(sol)
            report += "\n\n"

        report += "="*40 + "\n"
        return report


