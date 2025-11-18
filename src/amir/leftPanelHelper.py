import tkinter as tk
from tkinter import ttk
import constants
import NQueenSolver
import globals as g
import report_helper

def generate_left_panel(parent, root):

    left = tk.Frame(parent, bg=constants.BG_COLOR)
    left.grid(row=0, column=0, sticky="ns", padx=20, pady=20)

    create_n_selector(left)

    create_strategy_selector(left)

    create_solve_button(left, root)

    create_cancel_button(left)

    create_status_label(left)

    create_report_button(left, root)

    return left


def create_n_selector(left):
    n_row = tk.Frame(left)
    n_row.pack(anchor="w", pady=10)

    tk.Label(
        n_row,
        text="N",
        fg=constants.MAIN_COLOR,
        font=("Comic Sans MS", 14, "bold")
    ).pack(side="left", padx=(0, 10))

    g.n_var = tk.StringVar(value="4")

    ttk.Combobox(
        n_row,
        textvariable=g.n_var,
        state="readonly",
        values=constants.N_VALUES,
        width=5
    ).pack(side="left")

def create_strategy_selector(left):
    tk.Label(
        left,
        text="strategies",
        fg=constants.MAIN_COLOR,
        font=("Comic Sans MS", 14, "bold")
    ).pack(pady=10)

    g.strategy_var = tk.StringVar(value=constants.ALGO_BACKTRACKING)

    ttk.Combobox(
        left,
        textvariable=g.strategy_var,
        state="readonly",
        values=constants.ALGO_LIST,
        width=15
    ).pack()

def create_solve_button(left, root):
    tk.Button(
        left,
        text="Solve",
        command=lambda: NQueenSolver.solve(root),
        fg="white",
        bg=constants.SECONDARY_COLOR,
    ).pack(pady=20)

def create_cancel_button(left):
    tk.Button(
        left,
        text="Cancel",
        command=NQueenSolver.cancel_operation,
        fg="white",
        bg="red",
    ).pack(pady=5)


def create_report_button(left, root):
    tk.Button(
        left,
        text="Report",
        command=lambda: report_helper.start_report(root),
        fg="black",
        bg="#EBEFF5",
        bd=1,
        relief="solid"
    ).pack(pady=5)

def create_status_label(left):
    g.status_var = tk.StringVar(value="Ready")

    tk.Label(
        left,
        textvariable=g.status_var,
        fg="gray20",
        bg="white",
        font=("Comic Sans MS", 10, "italic")
    ).pack(pady=10, anchor="w")