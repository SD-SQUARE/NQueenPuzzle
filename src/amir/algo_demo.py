# algo_demo.py
import random
import globals as g


# =========================
# 1) BACKTRACKING (exact)
# =========================
def backtracking(n):
    res = []
    g.cancel_flag = False  # reset cancel flag

    def place(col, cur, rows, d1, d2):
        if g.cancel_flag:
            return

        if col > n:
            res.append(cur.copy())
            return

        for r in range(1, n + 1):
            print("---help---")
            if g.cancel_flag:
                return

            if r in rows or (r - col) in d1 or (r + col) in d2:
                continue

            cur.append(r)
            rows.add(r)
            d1.add(r - col)
            d2.add(r + col)

            place(col + 1, cur, rows, d1, d2)

            cur.pop()
            rows.remove(r)
            d1.remove(r - col)
            d2.remove(r + col)

    place(1, [], set(), set(), set())
    return res


# =========================
# Helpers for meta-heuristics
# =========================
def random_board(n):
    """Create random board: list of rows [1..n] for each column."""
    return [random.randint(1, n) for _ in range(n)]


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

    start = random_board(n)
    start_h = heuristic(start)

    # if already solution
    if start_h == 0:
        return [start]

    open_list = [(start_h, start)]
    visited = set()
    iterations = 0

    while open_list:
        if g.cancel_flag:
            return []

        # sort by heuristic (smallest first)
        open_list.sort(key=lambda x: x[0])
        h, board = open_list.pop(0)

        key = tuple(board)
        if key in visited:
            continue
        visited.add(key)

        if h == 0:  # found solution
            return [board]

        iterations += 1
        if iterations > max_iter:
            break

        for nb in generate_neighbors(board):
            if g.cancel_flag:
                return []
            k = tuple(nb)
            if k in visited:
                continue
            open_list.append((heuristic(nb), nb))

    # no solution found
    return []


# =========================
# 3) HILL-CLIMBING
# =========================
def hill_climbing(n, max_steps=1000, restarts=20):
    """
    Simple hill-climbing with random restarts.
    Returns [solution] or [].
    """
    g.cancel_flag = False

    for _ in range(restarts):
        if g.cancel_flag:
            return []

        current = random_board(n)
        current_h = heuristic(current)

        steps = 0
        while steps < max_steps and current_h > 0 and not g.cancel_flag:
            neighbors = generate_neighbors(current)
            # pick neighbor with best (lowest) heuristic
            best_neighbor = min(neighbors, key=heuristic)
            best_h = heuristic(best_neighbor)

            # if no improvement -> local optimum
            if best_h >= current_h:
                break

            current, current_h = best_neighbor, best_h
            steps += 1

        if current_h == 0:
            return [current]

    return []


# =========================
# 4) "CULTURAL" (simple evolutionary search)
# =========================
def cultural(n, population_size=30, generations=200, mutation_rate=0.2):
    """
    Simple evolutionary-like search (not a full academic cultural algorithm,
    but good as a 'cultural' demo).
    Returns [solution] or [].
    """
    g.cancel_flag = False

    # init population
    population = [random_board(n) for _ in range(population_size)]

    for gen in range(generations):
        if g.cancel_flag:
            return []

        # evaluate population
        scored = [(heuristic(b), b) for b in population]
        scored.sort(key=lambda x: x[0])

        best_h, best_board = scored[0]
        if best_h == 0:
            return [best_board]

        # belief (best part of population)
        elite_count = max(2, population_size // 3)
        elites = [b for _, b in scored[:elite_count]]

        # create new population from elites with mutation
        new_population = elites.copy()

        while len(new_population) < population_size:
            if g.cancel_flag:
                return []

            parent = random.choice(elites)
            child = parent.copy()

            if random.random() < mutation_rate:
                # mutate: move a queen in a random column
                col = random.randint(0, n - 1)
                child[col] = random.randint(1, n)

            new_population.append(child)

        population = new_population

    return []  # no solution found
