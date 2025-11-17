import numpy as np
from random import choice
from time import perf_counter

def ensure_N(n): 
    return max(4, int(n))

def random_state(N):
    return np.random.randint(0, N, size=N)

def board_from_state(state):
    N = state.size
    b = np.zeros((N, N), dtype=int)
    b[state, np.arange(N)] = 1
    return b

def objective(state):
    """Number of attacking pairs (vectorized)."""
    N = state.size
    cols = np.arange(N)
    rows = np.bincount(state, minlength=N)
    d1 = np.bincount(state - cols + (N-1), minlength=2*N-1)
    d2 = np.bincount(state + cols, minlength=2*N-1)
    comb2 = lambda x: (x * (x - 1)) // 2
    return int(comb2(rows).sum() + comb2(d1).sum() + comb2(d2).sum())

def best_neighbor(state):
    """Return (best_state, best_obj). Examines all single-column moves."""
    N = state.size
    cur_obj = objective(state)
    best_obj = cur_obj
    best_state = state.copy()
    for col in range(N):
        orig = state[col]
        for r in range(N):
            if r == orig:
                continue
            state[col] = r
            obj = objective(state)
            if obj < best_obj:
                best_obj = obj
                best_state = state.copy()
        state[col] = orig
    return best_state, best_obj

def hill_climb(N, max_restarts=50, max_sideways=100, max_iterations=10000):
    for restart in range(max_restarts):
        state = random_state(N)
        side_count = 0
        for it in range(max_iterations):
            cur_obj = objective(state)
            if cur_obj == 0:
                return state, board_from_state(state)
            neigh_state, neigh_obj = best_neighbor(state)
            if neigh_obj < cur_obj:
                state = neigh_state
                side_count = 0
            elif neigh_obj == cur_obj and side_count < max_sideways:
                # allow sideways move
                candidates = []
                for col in range(N):
                    orig = state[col]
                    for r in range(N):
                        if r == orig:
                            continue
                        state[col] = r
                        if objective(state) == neigh_obj:
                            candidates.append(state.copy())
                    state[col] = orig
                if candidates:
                    state = choice(candidates)
                    side_count += 1
                else:
                    break
            else:
                break  # stuck -> restart
    return None, None

if __name__ == "__main__":
    # Ask user for N and disallow N < 4
    try:
        N_input = int(input("Enter N (size of the chessboard): "))
    except ValueError:
        print("Invalid input. Please enter an integer (e.g. 8).")
        raise SystemExit(1)

    if N_input < 4:
        print("❌ N must be at least 4. No solutions exist for N < 4.")
    else:
        N = ensure_N(N_input)
        print(f"Solving {N}-Queens... (this may take a moment for large N)")
        t0 = perf_counter()
        sol_state, sol_board = hill_climb(N)
        t1 = perf_counter()
        elapsed = t1 - t0

        if sol_state is None:
            print("No solution found (try increasing restarts/sideways/max iterations).")
        else:
            print("\nstate:", *sol_state.tolist())
            for row in sol_board:
                print(*row.tolist())
            print(f"\nTime to find solution: {elapsed:.6f} seconds ({elapsed*1000:.1f} ms)")
