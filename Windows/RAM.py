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
from Windows.Base import BaseChild
import wmi


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"
__description__ = "System monitor"


class RAM(BaseChild):
    def __init__(self, root_class, core_label):
        super().__init__(root_class)
        self.history_length = 800
        self.height_per_section = 30
        self.width = self.child_weight + 500
        self.height = self.height_per_section + 10

        self.child_window.title(f"{core_label} Details")
        self.child_window.geometry(f"{self.width}x{self.height+100}+{self.x_child_pos}+{self.y_child_pos - 40}")

        c = wmi.WMI()
        for mem in c.Win32_PhysicalMemory():
            label = tk.Label(self.child_window, text=f"Capacity: {int(mem.Capacity) / (1024 ** 3):.2f} GB", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Speed: {mem.Speed} MHz", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Manufacturer: {mem.Manufacturer}", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Part Number: {mem.PartNumber.strip()}", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        self.canvas = tk.Canvas(self.child_window, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.pack()

        self.ram_history = [0]*self.history_length
        self.lines = [[] for _ in range(1)]  # зберігає id ліній

        self.ram_color = 'skyblue'

        self.update_thread = threading.Thread(target=self.update_usage)
        self.update_thread.daemon = True
        self.update_thread.start()

    def show(self):
        self.child_window.deiconify()
        self.child_window.lift()

    def hide(self):
        self.child_window.withdraw()

    def update_usage(self):
        while True:
            ram = psutil.virtual_memory().percent

            self.ram_history.append(ram)
            if len(self.ram_history) > self.history_length:
                self.ram_history.pop(0)

            self.draw_graph()
            time.sleep(1)

    def draw_graph(self):
        x_offset = 0  # горизонтальне розміщення
        core = 0

        # створити лінії, якщо ще не створено
        if len(self.lines[core]) < self.history_length - 1:
            for y in range(1, len(self.ram_history)):
                x1 = x_offset + (y - 1)
                x2 = x_offset + y
                y1 = self.height - (self.ram_history[y - 1] / 100) * self.height_per_section
                y2 = self.height - (self.ram_history[y] / 100) * self.height_per_section
                line = self.canvas.create_line(x1, y1, x2, y2, fill=self.ram_color, width=2)
                self.lines[core].append(line)
        else:
            # оновити координати існуючих ліній
            for y in range(1, self.history_length):
                x1 = x_offset + (y - 1)
                x2 = x_offset + y
                y1 = self.height - (self.ram_history[y - 1] / 100) * self.height_per_section
                y2 = self.height - (self.ram_history[y] / 100) * self.height_per_section
                self.canvas.coords(self.lines[core][y - 1], x1, y1, x2, y2)

        # оновити текст під кожним графіком
        tag = f"core_text_{core}"
        self.canvas.delete(tag)
        self.canvas.create_text(x_offset + 2, self.height - 25, anchor='sw', fill='white',
                                font=('Segoe UI', 8), text=f"RAM: {self.ram_history[-1]:.0f}%", tags=tag)
