# main_screen.py
import tkinter as tk
import leftPanelHelper
import solution_list_helper
import board_panel_helper 
import globals as g
import constants


def show_main_screen(root):

    frame = tk.Frame(root, bg=constants.BG_COLOR,
                     highlightthickness=3, highlightbackground=constants.SECONDARY_COLOR)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # ---- Top bar for timer (uses pack only) ----
    top_bar = tk.Frame(frame, bg=constants.BG_COLOR)
    top_bar.pack(fill="x", pady=(5, 15))

    # ---- Main grid area ----
    content = tk.Frame(frame, bg=constants.BG_COLOR)
    content.pack(expand=True, fill="both")

    # LEFT PANEL
    leftPanelHelper.generate_left_panel(content, root)

    # SOLUTION LIST & BOARD PANEL (inside grid)
    solution_list_helper.generate_solution_list(content)
    board_panel_helper.generate_board_panel(
        content, default_n=constants.DEFAULT_BOARD_PANEL_NUM
    )
