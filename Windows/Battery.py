# -- coding: utf-8 --
from __future__ import unicode_literals
import psutil
import tkinter as tk
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
        self.bat_history = [0] * self.history_length
        self.lines = [[] for _ in range(1)]  # зберігає id ліній
        self.bat_color = 'skyblue'
        self.c = wmi.WMI(namespace="root\\CIMV2")
        self.t = wmi.WMI(moniker="//./root/wmi")

        self.child_window.title(f"{core_label} Details")
        self.child_window.geometry(f"{self.width}x{self.height+325}+{self.x_child_pos}+{self.y_child_pos - 265}")

        # self.canvas_volts = tk.Canvas(self.child_window, width=self.width, height=self.height+200, bg='black', highlightthickness=0)
        # self.canvas_volts.pack()
        self.canvas = tk.Canvas(width=self.width, height=self.height, **self.args_canvas_create)
        self.canvas.pack()

        self._create_labels()
        self._update_labels()
        self._update_usage()

    def _update_usage(self):
        battery = psutil.sensors_battery()

        self.bat_history.append(battery.percent)
        if len(self.bat_history) > self.history_length:
            self.bat_history.pop(0)

        if self._build_flag:
            self._draw_graph()

        self.child_window.after(3000, self._update_usage)

    def _update_labels(self):
        batts1 = self.c.CIM_Battery(Caption='Portable Battery')
        for i, b in enumerate(batts1):
            _message = f"Battery {i} Design Capacity: {b.DesignCapacity or 0} mWh"
            self._design_capacity_label.config(text=_message)
        batts = self.t.ExecQuery('Select * from BatteryFullChargedCapacity')
        for i, b in enumerate(batts):
            _message = f"Battery {i} Fully Charged Capacity: {b.FullChargedCapacity} mWh"
            self._real_capacity_label.config(text=_message)
        batts = self.t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batts):
            _message = f"Name:                {b.InstanceName}"
            self._instance_name_label.config(text=_message)
            _message = f"PowerOnline:         {b.PowerOnline}"
            self._power_online_label.config(text=_message)
            _message = f"Discharging:       {b.Discharging}"
            self._discharging_label.config(text=_message)
            _message = f"Charging:          {b.Charging}"
            self._charging_label.config(text=_message)
            _message = f"Voltage:           {b.Voltage / 1000} V"
            self._voltage_label.config(text=_message)
            _message = f"DischargeCurrent:  {b.DischargeRate / b.Voltage} A"
            self._discharge_current_label.config(text=_message)
            _message = f"ChargeCurrent:     {b.ChargeRate / b.Voltage} A"
            self._charge_current_label.config(text=_message)
            _message = f"DischargeRate:     {b.DischargeRate / 1000} W"
            self._discharge_rate_label.config(text=_message)
            _message = f"ChargeRate:        {b.ChargeRate / 1000} W"
            self._charge_rate_label.config(text=_message)
            _message = f"RemainingCapacity: {b.RemainingCapacity / 1000} W"
            self._remaining_capacity_label.config(text=_message)
            _message = f"Active:            {b.Active}"
            self._active_label.config(text=_message)
            _message = f"Critical:          {b.Critical}"
            self._critical_label.config(text=_message)

        self.child_window.after(1000, self._update_labels)

    def _draw_graph(self):
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

    def _create_labels(self):
        self._design_capacity_label = tk.Label(text="-", **self.args_label_create)
        self._design_capacity_label.pack(**self.args_label_pack)

        self._real_capacity_label = tk.Label(text="-", **self.args_label_create)
        self._real_capacity_label.pack(**self.args_label_pack)

        self._instance_name_label = tk.Label(text="-", **self.args_label_create)
        self._instance_name_label.pack(**self.args_label_pack)

        self._power_online_label = tk.Label(text="-", **self.args_label_create)
        self._power_online_label.pack(**self.args_label_pack)

        self._discharging_label = tk.Label(text="-", **self.args_label_create)
        self._discharging_label.pack(**self.args_label_pack)

        self._charging_label = tk.Label(text="-", **self.args_label_create)
        self._charging_label.pack(**self.args_label_pack)

        self._voltage_label = tk.Label(text="-", **self.args_label_create)
        self._voltage_label.pack(**self.args_label_pack)

        self._discharge_current_label = tk.Label(text="-", **self.args_label_create)
        self._discharge_current_label.pack(**self.args_label_pack)

        self._charge_current_label = tk.Label(text="-", **self.args_label_create)
        self._charge_current_label.pack(**self.args_label_pack)

        self._discharge_rate_label = tk.Label(text="-", **self.args_label_create)
        self._discharge_rate_label.pack(**self.args_label_pack)

        self._charge_rate_label = tk.Label(text="-", **self.args_label_create)
        self._charge_rate_label.pack(**self.args_label_pack)

        self._remaining_capacity_label = tk.Label(text="-", **self.args_label_create)
        self._remaining_capacity_label.pack(**self.args_label_pack)

        self._active_label = tk.Label(text="-", **self.args_label_create)
        self._active_label.pack(**self.args_label_pack)

        self._critical_label = tk.Label(text="-", **self.args_label_create)
        self._critical_label.pack(**self.args_label_pack)
