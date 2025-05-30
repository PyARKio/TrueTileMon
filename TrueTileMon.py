# -- coding: utf-8 --
from __future__ import unicode_literals
import psutil
import tkinter as tk
import threading
import time
import random
from Windows.Root import Root
from Windows.Mouse import Mouse
from Windows.CPU import CPU
from Windows.RAM import RAM
from Windows.Battery import Battery


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"
__description__ = "System monitor"


class TrueTileMon:
    def __init__(self):
        self.info_window = None
        self.taskbar_height = 48  # типова висота панелі задач

        self.root_class = Root(self.taskbar_height)
        self.root_window = self.root_class.root

        self.mouse = Mouse(self.root_class, "Mouse")
        self.cpu = CPU(self.root_class, "CPU")
        self.ram = RAM(self.root_class, "RAM")
        self.battery = Battery(self.root_class, "Battery")

        self.mouse_label = self.root_class.create_tile("Mouse", on_click=self.open_info_window)
        self.cpu_label = self.root_class.create_tile("CPU", on_click=self.open_info_window)
        self.ram_label = self.root_class.create_tile("RAM", on_click=self.open_info_window)
        self.battery_label = self.root_class.create_tile("BAT", on_click=self.open_info_window)

        self.root_class.resize_and_position()

        threading.Thread(target=self.update_info, daemon=True).start()

        self.root_window.mainloop()

    def open_info_window(self, core_label):
        # Якщо вікно вже існує і ще відкрите — закрити
        if self.info_window:
            if self.info_window.child_window.winfo_exists():
                self.info_window.hide()
                self.info_window = None
                return

        # Інакше створити нове
        if core_label == "Mouse":
            self.mouse.show()
            self.info_window = self.mouse
        elif core_label == "CPU":
            self.cpu.show()
            self.info_window = self.cpu
        elif core_label == "RAM":
            self.ram.show()
            self.info_window = self.ram
        elif core_label == "BAT":
            self.battery.show()
            self.info_window = self.battery

        # # Якщо вікно закрили вручну — видалити з словника
        # def on_close():
        #     if self.info_window:
        #         self.info_window = None
        #     child_window.withdraw()
        #
        # # if child_window.winfo_exists():
        # child_window.protocol("WM_DELETE_WINDOW", on_close)

    def update_info(self):
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            battery = psutil.sensors_battery()

            # self.mouse_label.config(text=f"Mouse-> {self._mouse}")
            self.mouse_label.config(text=f"Mouse-> {self.mouse.mouse_state}")
            self.cpu_label.config(text=f"CPU: {cpu:.0f}%")
            self.ram_label.config(text=f"RAM: {ram:.0f}%")

            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                status = "⚡" if plugged else "🔋"
                self.battery_label.config(text=f"{status} {percent:.0f}%")
            else:
                self.battery_label.config(text="No Battery")

            time.sleep(1)


if __name__ == "__main__":
    TrueTileMon()
