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


class Battery(BaseChild):
    def __init__(self, root_class, core_label):
        super().__init__(root_class)
        self.history_length = 800
        self.height_per_section = 30
        self.width = self.child_weight + 500
        self.height = self.height_per_section + 10

        self.child_window.title(f"{core_label} Details")
        self.child_window.geometry(f"{self.width}x{self.height+325}+{self.x_child_pos}+{self.y_child_pos - 265}")

        self.c = wmi.WMI()
        self.t = wmi.WMI(moniker="//./root/wmi")

        batts1 = self.c.CIM_Battery(Caption='Portable Battery')
        for i, b in enumerate(batts1):
            _message = f"Battery {i} Design Capacity: {b.DesignCapacity or 0} mWh"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        batts = self.t.ExecQuery('Select * from BatteryFullChargedCapacity')
        for i, b in enumerate(batts):
            _message = f"Battery {i} Fully Charged Capacity: {b.FullChargedCapacity} mWh"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        batts = self.t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batts):
            _message = f"Name:                {b.InstanceName}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"PowerOnline:         {b.PowerOnline}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Discharging:       {b.Discharging}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Charging:          {b.Charging}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Voltage:           {b.Voltage / 1000} V"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"DischargeCurrent:  {b.DischargeRate / b.Voltage} A"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"ChargeCurrent:     {b.ChargeRate / b.Voltage} A"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"DischargeRate:     {b.DischargeRate / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"ChargeRate:        {b.ChargeRate / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"RemainingCapacity: {b.RemainingCapacity / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Active:            {b.Active}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Critical:          {b.Critical}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        self.canvas = tk.Canvas(self.child_window, width=self.width, height=self.height, bg='black',
                                highlightthickness=0)
        self.canvas.pack()

        self.bat_history = [0] * self.history_length
        self.lines = [[] for _ in range(1)]  # зберігає id ліній

        self.bat_color = 'skyblue'

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
            battery = psutil.sensors_battery()

            self.bat_history.append(battery.percent)
            if len(self.bat_history) > self.history_length:
                self.bat_history.pop(0)

            # if battery:
            #     percent = battery.percent
            #     plugged = battery.power_plugged
            #     status = "⚡" if plugged else "🔋"
            #     self.battery_label.config(text=f"{status} {percent:.0f}%")
            # else:
            #     self.battery_label.config(text="No Battery")

            self.draw_graph()
            time.sleep(1)

    def draw_graph(self):
        x_offset = 0  # горизонтальне розміщення
        core = 0

        # створити лінії, якщо ще не створено
        if len(self.lines[core]) < self.history_length - 1:
            for y in range(1, len(self.bat_history)):
                x1 = x_offset + (y - 1)
                x2 = x_offset + y
                y1 = self.height - (self.bat_history[y - 1] / 100) * self.height_per_section
                y2 = self.height - (self.bat_history[y] / 100) * self.height_per_section
                line = self.canvas.create_line(x1, y1, x2, y2, fill=self.bat_color, width=2)
                self.lines[core].append(line)
        else:
            # оновити координати існуючих ліній
            for y in range(1, self.history_length):
                x1 = x_offset + (y - 1)
                x2 = x_offset + y
                y1 = self.height - (self.bat_history[y - 1] / 100) * self.height_per_section
                y2 = self.height - (self.bat_history[y] / 100) * self.height_per_section
                self.canvas.coords(self.lines[core][y - 1], x1, y1, x2, y2)

        # оновити текст під кожним графіком
        tag = f"core_text_{core}"
        self.canvas.delete(tag)
        self.canvas.create_text(x_offset + 2, self.height - 25, anchor='sw', fill='white',
                                font=('Segoe UI', 8), text=f"Battery: {self.bat_history[-1]:.0f}%", tags=tag)

    def _update_labels(self):
        batts1 = self.c.CIM_Battery(Caption='Portable Battery')
        for i, b in enumerate(batts1):
            _message = f"Battery {i} Design Capacity: {b.DesignCapacity or 0} mWh"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        batts = self.t.ExecQuery('Select * from BatteryFullChargedCapacity')
        for i, b in enumerate(batts):
            _message = f"Battery {i} Fully Charged Capacity: {b.FullChargedCapacity} mWh"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        batts = self.t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batts):
            _message = f"Name:                {b.InstanceName}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"PowerOnline:         {b.PowerOnline}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Discharging:       {b.Discharging}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Charging:          {b.Charging}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Voltage:           {b.Voltage / 1000} V"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"DischargeCurrent:  {b.DischargeRate / b.Voltage} A"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"ChargeCurrent:     {b.ChargeRate / b.Voltage} A"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"DischargeRate:     {b.DischargeRate / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"ChargeRate:        {b.ChargeRate / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"RemainingCapacity: {b.RemainingCapacity / 1000} W"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Active:            {b.Active}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

            _message = f"Critical:          {b.Critical}"
            label = tk.Label(self.child_window, text=_message, fg="white", bg="#1e1e1e", font=("Segoe UI", 10),
                             anchor='w')
            label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

