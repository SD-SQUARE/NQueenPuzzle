import tkinter as tk
import globals as g
import solution_drawer
import constants

def generate_solution_list(parent):

    mid = tk.Frame(parent)
    mid.grid(row=0, column=1, sticky="ns", padx=20)

    # Title
    tk.Label(
        mid,
        text="solutions",
        fg=constants.MAIN_COLOR,
        font=("Comic Sans MS", 16, "bold")
    ).pack()

    # Listbox
    g.listbox = tk.Listbox(
        mid,
        fg=constants.MAIN_COLOR,
        font=("Comic Sans MS", 12),
        width=18,
        height=16
    )
    g.listbox.pack()

    # Event binding
    g.listbox.bind("<<ListboxSelect>>",
                   lambda e: solution_drawer.draw_selected_solution())

    return mid
