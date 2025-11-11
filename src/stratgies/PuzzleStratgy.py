from abc import ABC, abstractmethod

class PuzzleStratgy(ABC):

    @abstractmethod
    def solve(self, N = 4):
        pass
    
    @abstractmethod
    def generateReport(self, N = 4):
        pass

    @staticmethod
    def isSafe(self, board, row, col, N):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, N, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True
