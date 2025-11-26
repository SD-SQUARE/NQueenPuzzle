# main_screen.py
import tkinter as tk
import solution_drawer
import board_drawer
import leftPanelHelper
import solution_list_helper
import board_panel_helper 
import globals as g
import constants


def show_main_screen(root):

    frame = tk.Frame(root, bg=constants.BG_COLOR,
                     highlightthickness=3, highlightbackground="black")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    leftPanelHelper.generate_left_panel(frame, root)
    
    solution_list_helper.generate_solution_list(frame)

    board_panel_helper.generate_board_panel(frame, default_n=constants.DEFAULT_BOARD_PANEL_NUM)