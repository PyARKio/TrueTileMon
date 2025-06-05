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


class BaseChild:
    def __init__(self, root_class):
        self._build_flag = False
        self.root_class = root_class
        self.root_window = self.root_class.root

        self.x_child_pos = 0
        self.y_child_pos = self.get_y_child()
        self.child_weight = 300
        self.child_height = 100

        self.child_window = tk.Toplevel(self.root_window)
        self.child_window.withdraw()
        self.child_window.overrideredirect(True)
        self.child_window.attributes("-topmost", True)
        self.child_window.attributes("-alpha", 0.72)
        self.child_window.configure(bg="#1e1e1e")
        self.child_window.geometry(f"{self.child_weight}x{self.child_height}+{self.x_child_pos}+{self.y_child_pos}")

        self.args_canvas_create = {"master": self.child_window, "bg": 'black', "highlightthickness": 0}
        self.args_label_create = {"master": self.child_window, "fg": "white", "bg": "#1e1e1e", "font": ("Segoe UI", 10),"anchor": "w"}
        self.args_label_pack = {"expand": True, "padx": 10, "pady": (0, 0), "anchor": 'w'}
        self.args_button_create = {"master": self.child_window, "fg": "white", "bg": "#333333", "relief": "flat", "bd": 0,
                                   "activebackground": "#444444", "activeforeground": "white", "font": ("Segoe UI", 10)}
        self.args_button_pack = {"side": "left", "padx": 3, "pady": 3}

    def get_y_child(self):
        return self.root_class.get_y_root() - 100

    def show(self):
        self._build_flag = True
        self.child_window.deiconify()
        self.child_window.lift()

    def hide(self):
        self._build_flag = False
        self.child_window.withdraw()


class BasePopup:
    def __init__(self, weight, height, x, y):
        self._x_pos = x
        self._y_pos = y
        self._weight = weight
        self._height = height

        self._popup = tk.Toplevel()
        self._popup.withdraw()
        self._popup.overrideredirect(True)
        self._popup.attributes("-topmost", True)
        self._popup.attributes("-alpha", 0.82)
        self._popup.configure(bg="#1e1e1e")
        self._popup.geometry(f"{self._weight}x{self._height}+{self._x_pos}+{self._y_pos}")

        self._label = tk.Label(self._popup, text="Mouse-> clicked!", fg="white", bg="#1e1e1e", font=("Segoe UI", 10))
        self._label.pack(expand=True, padx=20, pady=20)

    def show(self):
        self._popup.deiconify()
        self._popup.lift()

    def hide(self):
        self._popup.withdraw()

    def label(self, message):
        self._label.config(text=message)
