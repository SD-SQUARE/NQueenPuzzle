# splash_screen.py
import tkinter as tk
from tkinter import ttk
import constants
from PIL import Image, ImageTk

from main_screen import show_main_screen   # <-- after splash, go to main

# we keep a reference to the splash window in a global variable
splash_window = None

def create_splash(root):

    global splash_window

    # hide main window at the start
    root.withdraw()

    splash_window = tk.Toplevel(root)
    splash_window.overrideredirect(True)  # remove title bar

    width, height = 900, 600

    screen_w = splash_window.winfo_screenwidth()
    screen_h = splash_window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    splash_window.geometry(f"{width}x{height}+{x}+{y}")

    # Canvas to draw the design
    canvas = tk.Canvas(splash_window, bg=constants.MAIN_COLOR, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    image_path = constants.QUEEN_IMAGE
    
    # 1. Load and resize the image 
    pil_image = Image.open(image_path) # Load the image
    pil_image = pil_image.resize((constants.FIXED_IMAGE_SIZE, constants.FIXED_IMAGE_SIZE), Image.LANCZOS)
    
    # 2. Convert to PhotoImage and display on canvas
    tk_image = ImageTk.PhotoImage(pil_image)
    canvas.queen_image_ref = tk_image # KEEP THE REFERENCE HERE
    
    canvas.create_image(
        450,
        192,
        image=tk_image 
    )   
     
    # Text: n-queen puzzle
    canvas.create_text(
        width / 2,
        height * 0.55,
        text="n-queen puzzle",
        fill=constants.SECONDARY_COLOR,
        font=("Comic Sans MS", 28, "bold")  # change font if needed
    )

    # Text: ready?
    canvas.create_text(
        width / 2,
        height * 0.78,
        text="ready?",
        fill=constants.SECONDARY_COLOR,
        font=("Comic Sans MS", 28, "bold")
    )

    # after time → hide splash → show main
    def transition():
        splash_window.destroy()
        root.deiconify()
        show_main_screen(root)

    splash_window.after(constants.SPLASH_TIME, transition)




