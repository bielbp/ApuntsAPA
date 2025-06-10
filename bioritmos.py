import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime as dt
from datetime import timedelta
from time  import sleep

def biorritmos():
    figura = plt.figure(figsize=(8, 6))
    tb.Style.instance = None
    style = tb.Style("cyborg")
    style.configure(".", font=("Arial", 12, "Italic Bold"))
    win = style.master
    win.title("Vaya mierda de bioritmos")
    
    lienzo = FigureCanvasTkAgg(figure=figura, master=win).get_tk_widget()
    lienzo.pack(side=tk.LEFT)

    frameDades = tb.Frame(win, width=500)
    frameDades.pack(side=tk.RIGHT)

    





    win.mainloop()

if __name__ == "__main__":
    biorritmos()