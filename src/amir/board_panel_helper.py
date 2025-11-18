import tkinter as tk
import globals as g
import board_drawer
import constants


def generate_board_panel(parent, default_n=4):

    right = tk.Frame(parent, )
    right.grid(row=0, column=2, sticky="nsew")

    g.canvas = tk.Canvas(
        right,
        width=450,
        height=450,
        bg=constants.MAIN_COLOR,
        highlightthickness=0
    )
    g.canvas.pack(expand=True)

    # Draw initial board
    board_drawer.draw_board(default_n)

    return right
