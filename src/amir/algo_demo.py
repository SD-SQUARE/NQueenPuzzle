# algo_demo.py
import random
from CulturalAlgorithm import cultural_algorithm
from BestFirst import BestFirst
from BackTrack import backtrackingAlgo
from hillclimb import hill_climb
import globals as g


# =========================
# 1) BACKTRACKING (exact)
# =========================
import time
import globals as g

# algo_demo.py

import time
import globals as g

def backtracking(n, record_times=False, start_time=None):
    """
    If record_times == False  -> returns [solutions]
    If record_times == True   -> returns (solutions, times)
        where times[i] is the time (sec) when solution i was found
    """

    solutions, times = backtrackingAlgo(n, record_times=True)
 
    if record_times:
        return solutions, times  # Return both solutions and times for each solution
    
    return solutions



# =========================
# Helpers for meta-heuristics
# =========================


def heuristic(board):
    """
    Number of attacking queen pairs (lower is better).
    board = [row_of_col0, row_of_col1, ...] with rows 1..n
    """
    attacks = 0
    n = len(board)
    for c1 in range(n):
        r1 = board[c1]
        for c2 in range(c1 + 1, n):
            r2 = board[c2]
            # same row OR same diagonal
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                attacks += 1
    return attacks


def generate_neighbors(board):
    """
    Generate neighbors by moving one queen in its column
    to another row (1..n).
    """
    n = len(board)
    neighbors = []
    for c in range(n):
        current_row = board[c]
        for r in range(1, n + 1):
            if r == current_row:
                continue
            new_board = board.copy()
            new_board[c] = r
            neighbors.append(new_board)
    return neighbors


# =========================
# 2) BEST-FIRST SEARCH
# =========================
def best_first(n, max_iter=5000):
    """
    Greedy best-first search on heuristic.
    Returns [solution] or [].
    """
    g.cancel_flag = False

    solver = BestFirst()
    solution = solver.solve(n)

    if solution:
        solution = [x + 1 for x in solution]
        return [solution]

    # no solution found
    return []


# =========================
# 3) HILL-CLIMBING
# =========================
def hill_climbing(n, max_steps=1000, restarts=20):
    """
    Simple hill-climbing.
    Returns [solution] or [].
    """
    g.cancel_flag = False

    state, board, elapsed = hill_climb(n)

    print("state ====>", state)

    if state.any():
        state = [x + 1 for x in state]
        return [state]
    
    return []


# =========================
# 4) "CULTURAL" (simple evolutionary search)
# =========================
def cultural(n,time, population_size=30, generations=200, mutation_rate=0.2):
    """
    Simple evolutionary-like search (not a full academic cultural algorithm,
    but good as a 'cultural' demo).
    Returns [solution] or [].
    """
    solution, gen, time = cultural_algorithm(n, time, population_size= 50, time_limit_seconds=60) # one-minute limit
    
    if solution:
        return [solution]

    return []  # no solution found
