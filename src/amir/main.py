# main.py
import tkinter as tk
from splash_screen import create_splash

def main():
    root = tk.Tk()
    root.title("N-Queen Puzzle")

    # Start with splash screen (this will hide root at first)
    create_splash(root)

    root.mainloop()


if __name__ == "__main__":
    main()
