import tkinter as tk
from tkinter import ttk
import globals as g
import constants
import algo_demo
import board_drawer


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

    # ---- NORMAL SWITCH CASE ----
    if strategy == constants.ALGO_BACKTRACKING:
        g.solutions = algo_demo.backtracking(n)

    elif strategy == constants.ALGO_BEST_FIRST:
        g.solutions = algo_demo.best_first(n)

    elif strategy == constants.ALGO_HILL_CLIMB:
        g.solutions = algo_demo.hill_climbing(n)

    elif strategy == constants.ALGO_CULTURAL:
        g.solutions = algo_demo.cultural(n)

    else:
        g.solutions = []
        root.config(cursor="")
        if g.status_var is not None:
            g.status_var.set("Unknown strategy")
        return

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

    # ✅ done → restore cursor & loader text
    root.config(cursor="")
    if g.status_var is not None:
        g.status_var.set(f"Done: {len(g.solutions)} solution(s)")
    

def cancel_operation():
    g.cancel_flag = True
    if g.status_var is not None:
        g.status_var.set("Cancelling...")
