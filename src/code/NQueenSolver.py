import tkinter as tk
from tkinter import ttk
import globals as g
import constants
import algo_demo
import board_drawer
import time  # For measuring time


def solve(root):
    # start a NEW solve → reset cancel flag
    g.cancel_flag = False

    n = int(g.n_var.get())
    strategy = g.strategy_var.get()

    # 🔄 show loader text + wait cursor
    if g.status_var is not None:
        g.status_var.set("Solving...")
    root.config(cursor="watch")
    root.update_idletasks()

    # Record the start time of the solving process
    start_time = time.perf_counter()

    # ---- NORMAL SWITCH CASE ----
    if strategy == constants.ALGO_BACKTRACKING:
        g.solutions, solution_times = algo_demo.backtracking(
            n, record_times=True, start_time=start_time
        )
        end_time = time.perf_counter()

    elif strategy == constants.ALGO_BEST_FIRST:
        g.solutions = algo_demo.best_first(n)
        end_time = time.perf_counter()

    elif strategy == constants.ALGO_HILL_CLIMB:
        g.solutions = algo_demo.hill_climbing(n)
        end_time = time.perf_counter()

    elif strategy == constants.ALGO_CULTURAL:
        g.solutions = algo_demo.cultural(n, start_time)
        end_time = time.perf_counter()

    else:
        g.solutions = []
        root.config(cursor="")
        if g.status_var is not None:
            g.status_var.set("Unknown strategy")
        return

    # ---- CALCULATE TOTAL TIME ----
    elapsed_time = end_time - start_time

    # user pressed cancel while solving
    if g.cancel_flag:
        root.config(cursor="")
        if g.status_var is not None:
            g.status_var.set("Cancelled")
        return

    # ---- UPDATE LISTBOX ----
    g.listbox.delete(0, tk.END)
    for i, sol in enumerate(g.solutions, start=1):
        g.listbox.insert(tk.END, f"solution {i:02d}")

    board_drawer.draw_board(n)

    # done => restore cursor & loader text
    root.config(cursor="")
    if g.status_var is not None:
        g.status_var.set(f"Done: {len(g.solutions)} solution(s)")

    # --- REPORTING RESULTS ---
    if strategy == constants.ALGO_BACKTRACKING:
        print("Backtracking Results:")
        for idx, (sol, sol_time) in enumerate(zip(g.solutions, solution_times), start=1):
            print(f"Solution {idx}: Time: {sol_time:.4f}s, Solution: {sol}")
    else:
        print(f"{strategy} Results:")
        print(f"Total Time: {elapsed_time:.4f}s, Solutions: {len(g.solutions)}")

    return elapsed_time


def cancel_operation():
    g.cancel_flag = True
    if g.status_var is not None:
        g.status_var.set("Cancelling...")
