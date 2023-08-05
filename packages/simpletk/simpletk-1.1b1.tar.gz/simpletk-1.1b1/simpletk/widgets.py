import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

# Button

def btn(root, text, command):
    btn = ttk.Button(root, text=text, command=command)
    btn.pack()


# Labels

def lbl(root, text):
    lbl = tk.Label(root, text=text)
    lbl.pack()


def lblf(root, text, font):
    lblf = tk.Label(root, text=text, font=font)
    lblf.pack()


# Entry widget

def ent(root):
    global entry
    entry = ttk.Entry(root)
    entry.pack()


def ent_get():
    return entry.get()


# MessageBoxes

def info(title, msg):
     mb.showinfo(title=title, message=msg)


def warn(title, msg):
     mb.showwarning(title=title, message=msg)


def err(title, msg):
     mb.showerror(title=title, message=msg)

