__author__ = 'marsson87'
__author_email__ = 'marsson87@gmail.com'

from tkinter import *
from tkinter import ttk
import tkinter as tk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, total_width, total_height, bgcolor, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.bgcolor = bgcolor
        canvas = tk.Canvas(self, width=total_width, height=total_height, highlightthickness=0)
        s = ttk.Style()
        s.configure('Vertical.TScrollbar', background=self.bgcolor)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(background=self.bgcolor)

        canvas.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=N + S + W)