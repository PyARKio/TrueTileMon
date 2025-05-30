# -- coding: utf-8 --
from __future__ import unicode_literals
import psutil
import tkinter as tk
import threading
import time
import random
from time import sleep
import mouse
import datetime


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"
__description__ = "System monitor"


class Root:
    def __init__(self, taskbar_height):
        self.taskbar_height = taskbar_height

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.48)
        self.root.configure(bg="#1e1e1e")

        self.x_root_pos = 0
        self.y_root_pos = self.get_y_root()

        self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.after(1000, self.keep_on_top)

        self.frame = tk.Frame(self.root, bg="#1e1e1e", height=self.taskbar_height)
        self.frame.pack(fill="both", expand=True)

        self.root.geometry(f"+{self.x_root_pos}+{self.y_root_pos}")

    def keep_on_top(self):
        self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.after(1000, self.keep_on_top)

    def get_y_root(self):
        screen_height = self.root.winfo_screenheight()
        return screen_height - self.taskbar_height

    def resize_and_position(self):
        self.root.update_idletasks()
        width = self.frame.winfo_reqwidth()
        self.root.geometry(f"{width}x{self.taskbar_height}+{self.x_root_pos}+{self.y_root_pos}")

    def create_tile(self, label_text, on_click=None):
        block = tk.Frame(self.frame, bg="#2c2c2c", padx=10, pady=5)
        block.pack(side="left", padx=1, pady=1)

        label = tk.Label(block, text=label_text + ": 0%", fg="white", bg="#2c2c2c",
                         font=("Segoe UI", 9, "bold"), anchor="center", width=10)
        label.pack()

        if on_click:
            label.bind("<Button-1>", lambda event: on_click(label_text))

        return label
