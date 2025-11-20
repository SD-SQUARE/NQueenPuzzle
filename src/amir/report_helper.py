# report_helper.py
import threading
import time
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import globals as g
import constants
import algo_demo



results_lock = threading.Lock()


# run backtracking algo once ===> each solution with its time
def _run_backtracking_once(n: int):
    start_time = time.perf_counter()
    solutions, solution_times = algo_demo.backtracking(
        n, record_times=True, start_time=start_time
    )

    with results_lock:
        g.algorithm_results[constants.ALGO_BACKTRACKING]["solutions"].extend(solutions)
        g.algorithm_results[constants.ALGO_BACKTRACKING]["times"].extend(solution_times)


def _run_meta_single(strategy: str, n: int):
    """Run a meta-heuristic algorithm once and record its total runtime."""
    start_time = time.perf_counter()

    if strategy == constants.ALGO_BEST_FIRST:
        sol = algo_demo.best_first(n)
    elif strategy == constants.ALGO_HILL_CLIMB:
        sol = algo_demo.hill_climbing(n)
    elif strategy == constants.ALGO_CULTURAL:
        sol = algo_demo.cultural(n, start_time)
    else:
        sol = []

    end_time = time.perf_counter()
    dt = end_time - start_time

    if sol:
        with results_lock:
            g.algorithm_results[strategy]["solutions"].append(sol)
            g.algorithm_results[strategy]["times"].append(dt)


def start_report(root):
    """
    Called from UI.
    - Backtracking: 1 thread (multiple solutions with their times)
    - Best-first, Hill-climb, Cultural: n threads each (each run = 1 thread)
    - All threads start in parallel, and we join them in a watcher thread.
    """
    if getattr(g, "is_reporting", False):
        return  # avoid double-click spam

    g.cancel_flag = False
    g.is_reporting = True

    # reset results
    for k in g.algorithm_results:
        g.algorithm_results[k]["solutions"].clear()
        g.algorithm_results[k]["times"].clear()

    if g.status_var:
        g.status_var.set("Running report...")
    root.config(cursor="watch")
    root.update_idletasks()

    n = int(g.n_var.get())  # board size, also number of runs for meta algos

    strategies_meta = [
        constants.ALGO_BEST_FIRST,
        constants.ALGO_HILL_CLIMB,
        constants.ALGO_CULTURAL,
    ]

    threads = []

    # ---- Backtracking: single thread ----
    t_back = threading.Thread(
        target=_run_backtracking_once,
        args=(n,),
        daemon=True,
    )
    threads.append(t_back)

    # ---- Meta-heuristics: n runs -> n threads per algorithm ----
    for strategy in strategies_meta:
        for _ in range(constants.N_Times):
            t = threading.Thread(
                target=_run_meta_single,
                args=(strategy, n),
                daemon=True,
            )
            threads.append(t)

    # ---- Start all threads in parallel ----
    for t in threads:
        t.start()

    # ---- Join all threads in a watcher so UI doesn't freeze ----
    def watcher():
        for t in threads:
            t.join()

        def finish_ui():
            root.config(cursor="")
            g.is_reporting = False
            if g.status_var:
                g.status_var.set("Report done")
            show_report_window(root, n)

        root.after(0, finish_ui)

    threading.Thread(target=watcher, daemon=True).start()


def show_report_window(root, n: int):
    """
    UI like the simple script:
      - X: time consumed (seconds)
      - Y: solution count / run index
      - Colors: r, b, y, m
      - Title: 'Algorithm Performance: Solutions vs Time for n = {n}'
    Embedded into a Tk Toplevel using FigureCanvasTkAgg.
    Also includes a 15-minute MM:SS timer specific to this window.
    """
    # if no data, do nothing
    if not any(g.algorithm_results[alg]["times"] for alg in g.algorithm_results):
        return

    win = tk.Toplevel(root)
    win.title("N-Queen Report: Solutions vs Time")

    # =======================
    # PLOTTING AREA
    # =======================
    fig, ax = plt.subplots(figsize=(10, 6))

    strategies = [
        constants.ALGO_BACKTRACKING,
        constants.ALGO_BEST_FIRST,
        constants.ALGO_HILL_CLIMB,
        constants.ALGO_CULTURAL,
    ]

    # Same colors as your simple script
    strategy_colors = {
        constants.ALGO_BACKTRACKING: 'r',  # Red
        constants.ALGO_BEST_FIRST:   'b',  # Blue
        constants.ALGO_HILL_CLIMB:   'y',  # Yellow
        constants.ALGO_CULTURAL:     'm',  # Magenta
    }

    for strategy in strategies:
        data = g.algorithm_results.get(strategy)
        if not data:
            continue

        times = data["times"]
        solutions = data["solutions"]

        # We only care about times for plotting
        if not times:
            continue

        color = strategy_colors.get(strategy, 'k')

        # Just like your script: y = 1..len(times)
        for idx, time_taken in enumerate(times):
            ax.scatter(time_taken, idx + 1, color=color, alpha=0.7, marker='o')

        # Legend entry
        ax.scatter([], [], color=color, label=strategy)

    ax.set_title(f'Algorithm Performance: Solutions vs Time for n = {n}', fontsize=14)
    ax.set_xlabel('Time Consumed (seconds)', fontsize=12)
    ax.set_ylabel('Solution Count', fontsize=12)

    ax.legend(title="Algorithms", fontsize=10, loc='upper left')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
