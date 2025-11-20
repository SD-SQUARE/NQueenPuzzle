import random
import heapq
import time

class BestFirst:
    def __init__(self):
        self.solutions = []
        self.board = []
        self.start_index_row = -1
        self.start_index_column = -1
        self.time_taken = 0
        self.steps = 0

    # ---------------------------------------------------------------
    # Simple N validation
    # ---------------------------------------------------------------
    def validate_n(self, N):
        if N < 4:
            raise ValueError("N must be >= 4 for N-Queens.")

    # ---------------------------------------------------------------
    # Heuristic: number of attacking queen pairs
    # ---------------------------------------------------------------
    def heuristic(self, board):
        conflicts = 0
        n = len(board)

        for i in range(n):
            for j in range(i + 1, n):
                # Same row OR on diagonal
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    # ---------------------------------------------------------------
    # Create neighbors by changing row of each column
    # ---------------------------------------------------------------
    def generate_children(self, board):
        children = []
        n = len(board)

        for col in range(n):
            original_row = board[col]
            for row in range(n):
                if row != original_row:
                    new_board = board.copy()
                    new_board[col] = row
                    children.append(new_board)
        return children

    # ---------------------------------------------------------------
    # Best-First Search algorithm
    # ---------------------------------------------------------------
    def solve(self, N=4):
        self.validate_n(N)

        start_time = time.time()
        self.steps = 0

        # Random initial board
        self.board = [random.randint(0, N - 1) for _ in range(N)]
        self.start_index_row = self.board[0]
        self.start_index_column = 0

        pq = []
        heapq.heappush(pq, (self.heuristic(self.board), self.board))

        visited = set()

        while pq:
            h, current = heapq.heappop(pq)
            self.steps += 1

            state = tuple(current)
            if state in visited:
                continue
            visited.add(state)

            # Goal found
            if h == 0:
                self.time_taken = time.time() - start_time
                self.solutions.append(current)
                return current

            for child in self.generate_children(current):
                c_state = tuple(child)
                if c_state not in visited:
                    heapq.heappush(pq, (self.heuristic(child), child))

        self.time_taken = time.time() - start_time
        return None

    # ---------------------------------------------------------------
    # Generate a readable solution report
    # ---------------------------------------------------------------
    def generateReport(self, N=4):
        if not self.solutions:
            return f"No solution found for N = {N}."

        board = self.solutions[-1]
        report = []

        report.append(f"Best-First Search Solution for N = {N}\n")
        report.append(f"Board (col -> row): {board}\n")
        report.append("Chessboard:")

        for r in range(N):
            line = ""
            for c in range(N):
                line += " Q " if board[c] == r else " . "
            report.append(line)

        report.append(f"\nStart Index: row = {self.start_index_row}, col = {self.start_index_column}")
        report.append(f"Solutions found: {len(self.solutions)}")
        report.append(f"Steps Taken: {self.steps}")
        report.append(f"Time Taken: {self.time_taken:.6f} seconds")

        return "\n".join(report)


# ---------------------------------------------------------------
# Run directly for testing
# ---------------------------------------------------------------
if __name__ == "__main__":
    try:
        N = int(input("Enter number of queens (N ≥ 4): "))
        solver = BestFirst()
        solver.solve(N)
        print(solver.generateReport(N))

    except ValueError:
        print("Invalid input! Please enter an integer value ≥ 4.")
