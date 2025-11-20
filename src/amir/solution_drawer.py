import globals as g
import board_drawer 
import constants

# [1,2,4,3]
def draw_solution(sol):
    board_drawer.draw_board(len(sol))
    cell = 50
    margin = 20

    for c, r in enumerate(sol):
        x = margin + (c * cell) + cell/2
        y = margin + ((r-1) * cell) + cell/2
        g.canvas.create_text(x, y, text=constants.QUEEN_LOGO,
                           fill= constants.SECONDARY_COLOR,
                           font=("Comic Sans MS", 28, "bold"))


def draw_selected_solution():
    sel = g.listbox.curselection()
    if not sel:
        return
    idx = sel[0]
    draw_solution(g.solutions[idx])

