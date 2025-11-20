import globals as g
import constants

def draw_board(n):
    g.canvas.delete("all")
    cell = 50
    margin = 20

    for c in range(n):
        for r in range(n):
            x1 = margin + c*cell
            y1 = margin + r*cell
            x2 = x1 + cell
            y2 = y1 + cell
            g.canvas.create_rectangle(x1, y1, x2, y2, 
                                    outline=constants.SECONDARY_COLOR , width=2)



