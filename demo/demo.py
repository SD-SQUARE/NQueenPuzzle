# TODO<*>: Revise algorithm descriptions in demo

"""
N-Queens Visualizer (Tkinter) — Backtracking, Hill-Climbing, Best-First, Cultural

Features:
- Animated visualization via generators
- Sidebar with found solutions
- Hover to highlight attack tiles
- Start / Pause / Reset controls
- Algorithm dropdown to choose algorithm
"""

import tkinter as tk
from tkinter import ttk
import time
from typing import List, Generator, Tuple, Optional, Set
import colorsys
import random
import heapq
import math

# ---------------------------- Generators / Algorithms ----------------------------

def n_queens_backtracking_generator(n: int) -> Generator[Tuple[str, Optional[tuple]], None, None]:
    cols = [False] * n
    d1 = [False] * (2 * n - 1)
    d2 = [False] * (2 * n - 1)
    positions = [-1] * n

    def backtrack(r: int):
        if r == n:
            yield ("found", tuple(positions))
            return
        for c in range(n):
            if not cols[c] and not d1[r + c] and not d2[r - c + n - 1]:
                cols[c] = d1[r + c] = d2[r - c + n - 1] = True
                positions[r] = c
                yield ("place", (r, c))
                yield from backtrack(r + 1)
                yield ("remove", (r, c))
                cols[c] = d1[r + c] = d2[r - c + n - 1] = False
                positions[r] = -1

    yield from backtrack(0)
    yield ("end", None)


# ---------- Utility: conflict heuristic ----------
def conflicts_of(positions: List[int]) -> int:
    n = len(positions)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if positions[i] == -1 or positions[j] == -1:
                continue
            if positions[i] == positions[j] or abs(positions[i] - positions[j]) == abs(i - j):
                count += 1
    return count


# ---------------------------- Hill-Climbing ----------------------------
def hill_climbing_generator(n: int, max_restarts: int = 50, max_steps_per_restart: int = 500) -> Generator[Tuple[str, Optional[tuple]], None, None]:
    """
    Random-restart hill climbing:
    - Start with random board (one queen per row)
    - For each row, consider moving queen to column with best (lowest) conflicts
    - If stuck (local minima), restart up to max_restarts
    """
    def random_board():
        return [random.randrange(n) for _ in range(n)]

    for restart in range(max_restarts):
        board = random_board()
        yield ("set", tuple(board))
        steps = 0
        while steps < max_steps_per_restart:
            steps += 1
            curr_conf = conflicts_of(board)
            if curr_conf == 0:
                yield ("found", tuple(board))
                return
            # find best single-row move
            best_moves = []
            best_conf = curr_conf
            for r in range(n):
                original = board[r]
                for c in range(n):
                    if c == original:
                        continue
                    board[r] = c
                    conf = conflicts_of(board)
                    if conf < best_conf:
                        best_conf = conf
                        best_moves = [(r, c)]
                    elif conf == best_conf:
                        best_moves.append((r, c))
                board[r] = original
            if best_conf < curr_conf and best_moves:
                move = random.choice(best_moves)
                board[move[0]] = move[1]
                yield ("set", tuple(board))
            else:
                # local minima, break to restart
                break
        # restart
        yield ("info", f"restart:{restart+1}")
    yield ("end", None)


# ---------------------------- Best-First Search ----------------------------
def best_first_generator(n: int, max_expansions: int = 20000) -> Generator[Tuple[str, Optional[tuple]], None, None]:
    """
    Best-first search using heuristic = number of conflicts.
    State representation: tuple of length n (column per row). We'll allow -1 for unfilled rows,
    but we initialize with random full states (one queen per row).
    """
    def random_full_state():
        return tuple(random.randrange(n) for _ in range(n))

    visited: Set[Tuple[int, ...]] = set()
    heap: List[Tuple[int, Tuple[int, ...]]] = []

    # seed heap with a few random states for exploration
    seeds = max(2, min(10, n))
    for _ in range(seeds):
        s = random_full_state()
        h = conflicts_of(list(s))
        heapq.heappush(heap, (h, s))
        visited.add(s)
        yield ("set", s)

    expansions = 0
    while heap and expansions < max_expansions:
        h, state = heapq.heappop(heap)
        expansions += 1
        yield ("set", state)
        if h == 0:
            yield ("found", state)
            return
        # expand neighbours: move one queen in one row
        for r in range(n):
            for c in range(n):
                if c == state[r]:
                    continue
                new = list(state)
                new[r] = c
                tnew = tuple(new)
                if tnew in visited:
                    continue
                visited.add(tnew)
                hnew = conflicts_of(new)
                heapq.heappush(heap, (hnew, tnew))
        if expansions % 50 == 0:
            yield ("info", f"expansions:{expansions} heap:{len(heap)}")
    yield ("end", None)


# ---------------------------- Cultural Algorithm (simple) ----------------------------
def cultural_generator(n: int, pop_size: int = 30, generations: int = 1000) -> Generator[Tuple[str, Optional[tuple]], None, None]:
    """
    Simplified Cultural Algorithm:
    - Population of boards (one queen per row)
    - Belief space: for each row, preferred column probabilities based on best individuals
    - Recombine & mutate guided by belief
    """
    def random_board():
        return [random.randrange(n) for _ in range(n)]

    # init population
    population = [random_board() for _ in range(pop_size)]
    fitness = [conflicts_of(ind) for ind in population]

    for gen in range(generations):
        # choose best half
        paired = list(zip(fitness, population))
        paired.sort(key=lambda x: x[0])
        best_half = [ind for _, ind in paired[: max(2, pop_size // 2)]]

        # if any perfect
        if paired[0][0] == 0:
            yield ("found", tuple(paired[0][1]))
            return

        # update belief: per-row distribution of columns based on best_half
        belief = []
        for r in range(n):
            counts = [0] * n
            for ind in best_half:
                counts[ind[r]] += 1
            # convert to probabilities
            total = sum(counts) + 1e-9
            probs = [ (counts[c] + 1) / (total + n) for c in range(n) ]  # smoothing
            belief.append(probs)

        # produce offspring guided by belief
        newpop = []
        for _ in range(pop_size):
            child = []
            for r in range(n):
                probs = belief[r]
                # sample column by belief probabilities sometimes; otherwise random
                if random.random() < 0.8:
                    # roulette selection
                    accum = 0.0
                    pick = random.random()
                    for c, p in enumerate(probs):
                        accum += p
                        if pick <= accum:
                            child.append(c)
                            break
                else:
                    child.append(random.randrange(n))
            # mutation
            if random.random() < 0.15:
                r = random.randrange(n)
                child[r] = random.randrange(n)
            newpop.append(child)

        population = newpop
        fitness = [conflicts_of(ind) for ind in population]

        # show best of generation
        best_idx = min(range(len(fitness)), key=lambda i: fitness[i])
        best_board = population[best_idx]
        yield ("set", tuple(best_board))
        yield ("info", f"gen:{gen+1} best:{fitness[best_idx]}")

    # finished
    yield ("end", None)


# ---------------------------- Helpers ----------------------------

def hsv_to_hex(h: float, s: float, v: float) -> str:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return '#{0:02x}{1:02x}{2:02x}'.format(int(r*255), int(g*255), int(b*255))


# ---------------------------- Main GUI ----------------------------

class NQueensVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens Visual Backtracking & Search")
        self.minsize(760, 520)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # state
        self.n = 8
        self.delay_ms = 200
        self._gen = None
        self._running = False
        self._paused = False
        self.step_count = 0
        self.start_time = None
        self.elapsed_time_job = None
        self.current_positions: List[int] = []
        self.solutions: List[List[int]] = []
        self.solution_list_items = 0
        self.queen_colors: List[str] = []
        self.hovered_queen: Optional[Tuple[int, int]] = None  # (row, col) under cursor

        self.create_widgets()
        self.bind_events()
        self.reset()

    # ---------------- GUI layout ----------------

    def create_widgets(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)

        # Sidebar
        side = ttk.Frame(main, width=260)
        side.pack(side="left", fill="y", padx=(6,4), pady=6)
        ttk.Label(side, text="Solutions").pack(anchor="nw")
        self.sol_listbox = tk.Listbox(side, exportselection=False)
        self.sol_listbox.pack(fill="both", expand=True, pady=(4,4))
        self.sol_listbox.bind("<<ListboxSelect>>", self.on_solution_select)
        ttk.Button(side, text="Clear Solutions", command=self.clear_solutions).pack(fill="x", pady=(4,0))

        ttk.Separator(side, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(side, text="Algorithm Settings").pack(anchor="nw")
        ttk.Label(side, text="Algorithm:").pack(anchor="w", pady=(4,0))
        self.algo_combo = ttk.Combobox(side, values=["Backtracking", "Hill Climbing", "Best-First", "Cultural"], state="readonly")
        self.algo_combo.current(0)
        self.algo_combo.pack(fill="x", pady=(2,6))

        # Right
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        controls = ttk.Frame(right)
        controls.pack(side="top", fill="x", padx=6, pady=6)

        ttk.Label(controls, text="N:").pack(side="left")
        self.spin_n = ttk.Spinbox(controls, from_=4, to=16, width=5, command=self.on_n_change)
        self.spin_n.set(str(self.n))
        self.spin_n.pack(side="left", padx=(2, 8))

        ttk.Label(controls, text="Speed:").pack(side="left")
        self.speed_slider = ttk.Scale(controls, from_=10, to=800, orient="horizontal", command=self.on_speed_change)
        self.speed_slider.set(self.delay_ms)
        self.speed_slider.pack(side="left", padx=(2, 8), fill="x", expand=True)
        self.speed_label = ttk.Label(controls, text=f"{self.delay_ms} ms")
        self.speed_label.pack(side="left", padx=(2, 8))

        self.start_btn = ttk.Button(controls, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=4)
        self.pause_btn = ttk.Button(controls, text="Pause", command=self.toggle_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=4)
        self.reset_btn = ttk.Button(controls, text="Reset", command=self.reset)
        self.reset_btn.pack(side="left", padx=4)
        self.info_label = ttk.Label(controls, text="Steps: 0   Time: 0.000 s")
        self.info_label.pack(side="left", padx=(12,0))

        self.canvas = tk.Canvas(right, bg="#f0f0f0")
        self.canvas.pack(fill="both", expand=True, padx=6, pady=(0,6))

        footer = ttk.Frame(self)
        footer.pack(side="bottom", fill="x", padx=6, pady=6)
        self.status_label = ttk.Label(footer, text="Ready")
        self.status_label.pack(side="left")

    def bind_events(self):
        self.canvas.bind("<Configure>", lambda e: self.redraw_board())
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.bind("<space>", lambda e: self.toggle_pause())

    # ---------------- Events & actions ----------------

    def on_mouse_move(self, event):
        """Check if mouse is hovering over a queen."""
        n = self.n
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        pad = 8
        cell_size = min((width - pad * 2) / n, (height - pad * 2) / n)
        board_w = cell_size * n
        board_h = cell_size * n
        offset_x = (width - board_w) / 2
        offset_y = (height - board_h) / 2

        x = event.x - offset_x
        y = event.y - offset_y
        if 0 <= x < board_w and 0 <= y < board_h:
            c = int(x // cell_size)
            r = int(y // cell_size)
            if 0 <= r < n and 0 <= c < n:
                if r < len(self.current_positions) and self.current_positions[r] == c:
                    if self.hovered_queen != (r, c):
                        self.hovered_queen = (r, c)
                        self.redraw_board()
                        return
        if self.hovered_queen is not None:
            self.hovered_queen = None
            self.redraw_board()

    def on_mouse_leave(self, _):
        if self.hovered_queen is not None:
            self.hovered_queen = None
            self.redraw_board()

    def on_n_change(self):
        try:
            v = int(self.spin_n.get())
        except Exception:
            return
        self.n = max(4, min(16, v))
        self.reset()

    def on_speed_change(self, val):
        try:
            v = float(val)
        except Exception:
            return
        self.delay_ms = int(v)
        self.speed_label.config(text=f"{self.delay_ms} ms")

    # ---------------- Start / Reset / Pause ----------------

    def start(self):
        if self._running:
            return
        try:
            self.n = int(self.spin_n.get())
        except Exception:
            self.n = 8
            self.spin_n.set(str(self.n))

        algo = self.algo_combo.get()
        # create generator based on selection
        if algo == "Backtracking":
            self._gen = n_queens_backtracking_generator(self.n)
        elif algo == "Hill Climbing":
            self._gen = hill_climbing_generator(self.n, max_restarts=100, max_steps_per_restart=300)
        elif algo == "Best-First":
            self._gen = best_first_generator(self.n, max_expansions=10000)
        elif algo == "Cultural":
            self._gen = cultural_generator(self.n, pop_size=40, generations=1000)
        else:
            self._gen = n_queens_backtracking_generator(self.n)

        self._running = True
        self._paused = False
        self.step_count = 0
        self.current_positions = [-1] * self.n
        self.start_time = time.time()
        self.update_elapsed_time()

        self.queen_colors = [hsv_to_hex((i/self.n)%1.0, 0.65, 0.65) for i in range(self.n)]
        self.pause_btn.config(state="normal", text="Pause")
        self.start_btn.config(state="disabled")
        self.spin_n.config(state="disabled")
        self.status_label.config(text=f"Running ({self.algo_combo.get()})...")
        self.schedule_next_step()

    def schedule_next_step(self):
        if not self._running or self._paused:
            return
        try:
            action, payload = next(self._gen)
        except StopIteration:
            action, payload = ("end", None)

        if action == "place":
            r, c = payload
            self.current_positions[r] = c
            self.step_count += 1
        elif action == "remove":
            r, c = payload
            self.current_positions[r] = -1
            self.step_count += 1
        elif action == "set":
            pos = list(payload)
            # normalize length
            if len(pos) != self.n:
                pos = list(pos)[:self.n] + [-1] * max(0, self.n - len(pos))
            self.current_positions = pos
            self.step_count += 1
        elif action == "found":
            pos = list(payload)
            self.solutions.append(pos)
            self.solution_list_items += 1
            self.sol_listbox.insert("end", f"Solution {self.solution_list_items}")
            self.current_positions = pos.copy()
            self.step_count += 1
        elif action == "info":
            # small status info from generator (e.g., restarts or generation)
            self.status_label.config(text=str(payload))
        elif action == "end":
            self._running = False
            self.pause_btn.config(state="disabled")
            self.start_btn.config(state="normal")
            self.spin_n.config(state="normal")
            self.status_label.config(text="Finished")
            self.stop_elapsed_time()
            self.update_info_label()
            self.redraw_board()
            return

        self.update_info_label()
        self.redraw_board()
        self.after(self.delay_ms, self.schedule_next_step)

    def toggle_pause(self, *_):
        if not self._running:
            return
        self._paused = not self._paused
        if self._paused:
            self.pause_btn.config(text="Resume")
            self.status_label.config(text="Paused")
        else:
            self.pause_btn.config(text="Pause")
            self.status_label.config(text=f"Running ({self.algo_combo.get()})...")
            self.schedule_next_step()

    def reset(self):
        self._running = False
        self._paused = False
        self._gen = None
        self.step_count = 0
        self.current_positions = [-1] * self.n
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="Pause")
        self.spin_n.config(state="normal")
        self.hovered_queen = None
        self.stop_elapsed_time()
        self.update_info_label()
        self.redraw_board()

    def clear_solutions(self):
        self.solutions.clear()
        self.sol_listbox.delete(0, "end")
        self.solution_list_items = 0

    def on_solution_select(self, event):
        sel = event.widget.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self.solutions):
            self._running = False
            self.current_positions = self.solutions[idx].copy()
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.spin_n.config(state="normal")
            self.redraw_board()

    # ---------------- Info & Time ----------------

    def update_info_label(self):
        elapsed = 0.0
        if self.start_time and self._running:
            elapsed = time.time() - self.start_time
        self.info_label.config(text=f"Steps: {self.step_count}   Time: {elapsed:.3f} s")

    def update_elapsed_time(self):
        if not self._running:
            return
        self.update_info_label()
        self.elapsed_time_job = self.after(100, self.update_elapsed_time)

    def stop_elapsed_time(self):
        if self.elapsed_time_job:
            try:
                self.after_cancel(self.elapsed_time_job)
            except Exception:
                pass
            self.elapsed_time_job = None

    # ---------------- Drawing ----------------

    def redraw_board(self):
        self.canvas.delete("all")
        n = self.n
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        pad = 8
        cell_size = min((width - pad * 2) / n, (height - pad * 2) / n)
        board_w = cell_size * n
        board_h = cell_size * n
        offset_x = (width - board_w) / 2
        offset_y = (height - board_h) / 2

        # base board
        for r in range(n):
            for c in range(n):
                x0 = offset_x + c * cell_size
                y0 = offset_y + r * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                fill = "#F0D9B5" if (r + c) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="")

        # Hover highlight (attack tiles)
        if self.hovered_queen:
            r, c = self.hovered_queen
            # highlight all attack tiles in red/orange tones
            for rr in range(n):
                for cc in range(n):
                    if rr == r and cc == c:
                        continue
                    if rr == r or cc == c or abs(rr - r) == abs(cc - c):
                        x0 = offset_x + cc * cell_size
                        y0 = offset_y + rr * cell_size
                        x1 = x0 + cell_size
                        y1 = y0 + cell_size
                        # red/orange alternating tint
                        color = "#ff5555" if (rr + cc) % 2 == 0 else "#ff8844"
                        self.canvas.create_rectangle(x0+1, y0+1, x1-1, y1-1, fill=color, outline="")

        # Draw queens
        font_size = max(12, int(cell_size * 0.65))
        font = ("Segoe UI Symbol", font_size, "bold")
        for r in range(len(self.current_positions)):
            c = self.current_positions[r]
            if c < 0:
                continue
            x = offset_x + c * cell_size + cell_size/2
            y = offset_y + r * cell_size + cell_size/2
            base = self.queen_colors[r] if r < len(self.queen_colors) else "#222"
            if self.hovered_queen and (r, c) == self.hovered_queen:
                # glowing orange halo
                self.canvas.create_oval(x - cell_size*0.35, y - cell_size*0.35,
                                        x + cell_size*0.35, y + cell_size*0.35,
                                        fill="#ff9933", outline="")
            self.canvas.create_text(x, y, text="♛", font=font, fill=base)

    def on_close(self):
        self._running = False
        self.destroy()



if __name__ == "__main__":
    app = NQueensVisualizer()
    app.mainloop()
