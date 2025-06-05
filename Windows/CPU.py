# -- coding: utf-8 --
from __future__ import unicode_literals
import psutil
import tkinter as tk
import random
from Windows.Base import BaseChild
import wmi


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"
__description__ = "System monitor"


class CPU(BaseChild):
    def __init__(self, root_class, core_label):
        super().__init__(root_class)
        self.num_cores = psutil.cpu_count(logical=True)
        self.history_length = 100
        self.height_per_core = 30
        self.width = self.num_cores * self.history_length
        self.height = self.height_per_core + 10

        self.child_window.title(f"{core_label} Details")
        self.child_window.geometry(f"{self.width}x{self.height+100}+{self.x_child_pos}+{self.y_child_pos - 40}")

        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            label = tk.Label(self.child_window, text=f"Name: {cpu.Name.strip()}", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Cores: {cpu.NumberOfCores}", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Logical processors: {cpu.NumberOfLogicalProcessors}", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
            label = tk.Label(self.child_window, text=f"Max Clock Speed: {cpu.MaxClockSpeed} MHz", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        self.canvas = tk.Canvas(width=self.width, height=self.height, **self.args_canvas_create)
        self.canvas.pack()
        self.usage_history = [[0]*self.history_length for _ in range(self.num_cores)]
        self.lines = [[] for _ in range(self.num_cores)]  # зберігає id ліній
        self.colors = self.generate_colors()
        self.update_cpu()

    def generate_colors(self):
        base_colors = ['lime', 'cyan', 'orange', 'yellow', 'magenta']
        return [random.choice(base_colors) for _ in range(self.num_cores)]

    def update_cpu(self):
        usages = psutil.cpu_percent(percpu=True)
        for i in range(self.num_cores):
            self.usage_history[i].append(usages[i])
            if len(self.usage_history[i]) > self.history_length:
                self.usage_history[i].pop(0)

        if self._build_flag:
            self.draw_graph()

        self.child_window.after(1000, self.update_cpu)

    def draw_graph(self):
        for core in range(self.num_cores):
            history = self.usage_history[core]
            color = self.colors[core]
            x_offset = core * self.history_length  # горизонтальне розміщення

            # створити лінії, якщо ще не створено
            if len(self.lines[core]) < self.history_length - 1:
                for y in range(1, len(history)):
                    x1 = x_offset + (y - 1)
                    x2 = x_offset + y
                    y1 = self.height - (history[y - 1] / 100) * self.height_per_core
                    y2 = self.height - (history[y] / 100) * self.height_per_core
                    line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                    self.lines[core].append(line)
            else:
                # оновити координати існуючих ліній
                for y in range(1, self.history_length):
                    x1 = x_offset + (y - 1)
                    x2 = x_offset + y
                    y1 = self.height - (history[y - 1] / 100) * self.height_per_core
                    y2 = self.height - (history[y] / 100) * self.height_per_core
                    self.canvas.coords(self.lines[core][y - 1], x1, y1, x2, y2)

            # оновити текст під кожним графіком
            tag = f"core_text_{core}"
            self.canvas.delete(tag)
            self.canvas.create_text(x_offset + 2, self.height - 25, anchor='sw', fill='white',
                                    font=('Segoe UI', 8), text=f"Core {core}: {history[-1]:.0f}%", tags=tag)
