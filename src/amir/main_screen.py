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

    # create_main_timer_label(top_bar)
    # start_main_timer_once(root)

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

def _update_main_timer(root):
    """Tick every second."""
    if not g.main_timer_running:
        return

    mins = g.main_timer_seconds // 60
    secs = g.main_timer_seconds % 60

    # update UI
    if g.main_timer_label:
        g.main_timer_label.config(text=f"{mins:02d}:{secs:02d}")

    # stop if timer ends
    if g.main_timer_seconds <= 0:
        g.main_timer_running = False
        return

    # decrease by 1 second
    g.main_timer_seconds -= 1

    # schedule next tick
    root.after(1000, lambda: _update_main_timer(root))


def start_main_timer_once(root):
    """
    Start timer ONLY the first time.
    Solve should NOT reset it.
    """
    if g.main_timer_started_once:
        return

    g.main_timer_started_once = True
    g.main_timer_running = True
    _update_main_timer(root)


def create_main_timer_label(parent):
    """Create the timer label the first time the screen loads."""
    if g.main_timer_label is None:
        g.main_timer_label = tk.Label(
            parent,
            text="15:00",
            font=("Arial", 12),
            fg=constants.MAIN_COLOR,
        )
        g.main_timer_label.pack(side="top", anchor="ne", padx=10, pady=10)