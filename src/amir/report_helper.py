# report_helper.py
import threading
import time
import tkinter as tk   # for Toplevel

import globals as g
import constants
import algo_demo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def start_report(root):
    """Start running all algorithms in a background thread."""
    if g.is_reporting:   # avoid double-click spam
        return

    g.cancel_flag = False
    g.is_reporting = True
    g.report_data = {}

    if g.status_var is not None:
        g.status_var.set("Running report...")
    root.config(cursor="watch")
    root.update_idletasks()

    n = int(g.n_var.get())

    def worker():
        # map algo name -> function (same as in solve)
        algo_map = {
            constants.ALGO_BACKTRACKING: algo_demo.backtracking,
            constants.ALGO_BEST_FIRST:   algo_demo.best_first,
            constants.ALGO_HILL_CLIMB:   algo_demo.hill_climbing,
            constants.ALGO_CULTURAL:     algo_demo.cultural,
        }

        for name, func in algo_map.items():
            if g.cancel_flag:
                break

            t0 = time.perf_counter()
            sols = func(n)          # heavy work
            t1 = time.perf_counter()

            g.report_data[name] = {
                "time": t1 - t0,
                "solutions": len(sols),
            }

        g.is_reporting = False

        # back to main thread: show report window & reset UI
        def finish_ui():
            root.config(cursor="")
            if g.cancel_flag:
                if g.status_var is not None:
                    g.status_var.set("Report cancelled")
            else:
                if g.status_var is not None:
                    g.status_var.set("Report done")
                show_report_window(root)

        root.after(0, finish_ui)

    threading.Thread(target=worker, daemon=True).start()


def show_report_window(root):
    """Open a new window and plot time vs solutions for each algorithm."""

    if not g.report_data:
        return

    win = tk.Toplevel(root)
    win.title("N-Queen Report: Solutions vs Time")
    win.configure(bg="black")

    # Prepare data
    algo_names = []
    times = []
    sol_counts = []
    colors = []

    for name in constants.ALGO_LIST:
        data = g.report_data.get(name)
        if not data:
            continue
        algo_names.append(name)
        times.append(data["time"])
        sol_counts.append(data["solutions"])
        colors.append(constants.ALGO_COLORS.get(name, "white"))

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    # scatter points
    ax.scatter(times, sol_counts, s=80)

    # color each point and add labels
    for x, y, name, c in zip(times, sol_counts, algo_names, colors):
        ax.scatter(x, y, s=80, color=c)
        ax.text(x, y, f" {name}", color="white", fontsize=8, va="bottom")

    ax.set_xlabel("time consumed (seconds)", color="orange")
    ax.set_ylabel("solutions", color="lime")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")

    # embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)