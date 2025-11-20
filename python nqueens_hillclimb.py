import numpy as np
from random import choice
from time import perf_counter
from typing import Optional, Tuple


def ensure_N(n: int) -> int:
    return max(4, int(n))


def random_state(N: int) -> np.ndarray:
    return np.random.randint(0, N, size=N)


def board_from_state(state: np.ndarray) -> np.ndarray:
    N = state.size
    board = np.zeros((N, N), dtype=int)
    board[state, np.arange(N)] = 1
    return board


def objective(state: np.ndarray) -> int:

    N = state.size
    cols = np.arange(N)
    rows_count = np.bincount(state, minlength=N)
    d1 = np.bincount(state - cols + (N - 1), minlength=2 * N - 1)
    d2 = np.bincount(state + cols, minlength=2 * N - 1)
    comb2 = lambda x: (x * (x - 1)) // 2
    return int(comb2(rows_count).sum() + comb2(d1).sum() + comb2(d2).sum())


def best_neighbor(state: np.ndarray) -> Tuple[np.ndarray, int]:
    N = state.size
    best_obj = objective(state)
    best_state = state.copy()

    for col in range(N):
        orig_row = state[col]
        for r in range(N):
            if r == orig_row:
                continue
            state[col] = r
            obj = objective(state)
            if obj < best_obj:
                best_obj = obj
                best_state = state.copy()
        state[col] = orig_row

    return best_state, best_obj


def hill_climb(
    N: int,
    max_restarts: int = 50,
    max_sideways: int = 100,
    max_iterations: int = 10000,
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], float]:
    start_time = perf_counter()

    for restart in range(max_restarts):
        state = random_state(N)
        side_count = 0

        for it in range(max_iterations):
            cur_obj = objective(state)
            if cur_obj == 0:
                elapsed = perf_counter() - start_time
                return state, board_from_state(state), elapsed

            neigh_state, neigh_obj = best_neighbor(state)

            if neigh_obj < cur_obj:
                state = neigh_state
                side_count = 0
            elif neigh_obj == cur_obj and side_count < max_sideways:
                candidates = []
                for col in range(N):
                    orig_row = state[col]
                    for r in range(N):
                        if r == orig_row:
                            continue
                        state[col] = r
                        if objective(state) == neigh_obj:
                            candidates.append(state.copy())
                    state[col] = orig_row
                if candidates:
                    state = choice(candidates)
                    side_count += 1
                else:
                    break
            else:
                break
    elapsed = perf_counter() - start_time
    return None, None, elapsed


def _prompt_and_run():
    try:
        N_input = int(input("Enter N (size of the chessboard): "))
    except ValueError:
        print("Invalid input. Please enter an integer (e.g. 8).")
        raise SystemExit(1)

    if N_input < 4:
        print("N must be at least 4. No solutions exist for N < 4.")
        raise SystemExit(1)

    N = ensure_N(N_input)
    print(f"Solving {N}-Queens...")

    state, board, elapsed = hill_climb(N)

    print("state ===> ", state)

    if state is None:
        print("No solution found. Try increasing max_restarts/max_sideways/max_iterations.")
        print(f"Elapsed time: {elapsed:.6f} seconds")
    else:
        print("\nstate (column->row):", *state.tolist())
        for row in board:
            print(*row.tolist())
        print(f"\nTime to find solution: {elapsed:.6f} seconds ({elapsed*1000:.1f} ms)")


if __name__ == "__main__":
    _prompt_and_run()
