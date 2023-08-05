import tkinter as tk


root = tk.Tk()

# Window settings

def window(root, title, width, height):
    root.title(title)
    root.geometry(f'{width}x{height}')


def sizes(root, width, height):
    root.resizable(width=width, height=height)


# Mainloop

def loop(root):
        root.mainloop()

