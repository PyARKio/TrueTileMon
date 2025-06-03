# -- coding: utf-8 --
from __future__ import unicode_literals
from GeneralArsenal.Chronicler import log
import tkinter as tk
import threading
import time
import mouse
from Windows.Base import BaseChild, BasePopup
import ctypes


__author__ = 'PyARK'
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"
__description__ = "System monitor"


# ToDo: Date -> 28 травня 2025 14:42
# Done: додати логіку на відклюення/підключення детектора(додати ручний режим);
# ToDo: додати сетінги;
# ToDo: рефакторинг існуючого
# ToDo: Додати відображення часу що лишився до запуску клікера;
# ToDo: скільки часу вже працює клікер
# ToDo: Додати час роботи клікера (тобто, перестати клікати з 18:00)


class Mouse(BaseChild):
    INACTIVITY_TIMEOUT = 240  # 4 хвилини
    WARNING_WINDOW_TIMEOUT = INACTIVITY_TIMEOUT - 15
    CLICK_INTERVAL = 10  # 10 секунд

    def __init__(self, root_class, core_label):
        super().__init__(root_class)
        self.last_activity = time.time()
        self.stop_clicking = threading.Event()

        self._mouse_id = False
        self._detector_flag = True
        self.mouse_state = "OFF"
        self.detector_state = "ON"
        self.child_window.title(f"{core_label} Details")
        # self.child_window.geometry(f"{self.child_weight}x{self.child_height}+{self.x_child_pos}+{self.y_child_pos}")

        # args_dict = {"fg": "white", "bg": "#1e1e1e", "font": ("Segoe UI", 10), "anchor": "w"}
        # args_dict["text"] = f"Inactivity timeout: {Mouse.INACTIVITY_TIMEOUT} sec"

        self._inactivity_timeout_label = tk.Label(self.child_window, text=f"Inactivity timeout: {Mouse.INACTIVITY_TIMEOUT} sec", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
        self._inactivity_timeout_label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
        self._time_since_label = tk.Label(self.child_window, text="Time since: - sec", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
        self._time_since_label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')
        self._time_for_label = tk.Label(self.child_window, text="Time for: - sec", fg="white", bg="#1e1e1e", font=("Segoe UI", 10), anchor='w')
        self._time_for_label.pack(expand=True, padx=10, pady=(0, 0), anchor='w')

        self._mouse_stop_button = tk.Button(self.child_window, text=f"Mouse {self.mouse_state}", command=self.on_button_stop, fg="white", bg="#333333",
                        activebackground="#444444", activeforeground="white", relief="flat", bd=0, font=("Segoe UI", 10))
        self._mouse_stop_button.pack(side="left", padx=3, pady=3)

        self._cursor_detector_button = tk.Button(self.child_window, text=f"Detector-> {self.detector_state}", command=self.on_button_detector,
                        fg="white", bg="#333333", activebackground="#444444", activeforeground="white", relief="flat",
                        bd=0, font=("Segoe UI", 10))
        self._cursor_detector_button.pack(side="left", padx=3, pady=3)
        self._popup = BasePopup(weight=400, height=250, x=int((self.get_screen_size("x")/2)-200), y=int((self.get_screen_size("y")/2)-125))

        threading.Thread(target=self.activity_listener, daemon=True).start()
        threading.Thread(target=self.auto_clicker, daemon=True).start()

        log.warning(f"{self.get_screen_size('x')}, {self.get_screen_size('y')}")

    # +++ AUTODETECTOR ++++++++++++++++++
    def activity_listener(self):
        def on_event(e):
            if not self._detector_flag:
                mouse.unhook(on_event)
            elif isinstance(e, mouse.MoveEvent):
                try:
                    self._popup.hide()
                except Exception as err:
                    log.error(err)
                self.last_activity = time.time()
                self.stop_clicking.set()  # зупинити клікання
        mouse.hook(on_event)

    def auto_clicker(self):
        while self._detector_flag:
            time_since = time.time() - self.last_activity
            # self._time_since_label.config(text=f"Time since: {time_since} sec")
            if time_since > Mouse.WARNING_WINDOW_TIMEOUT:
                log.warning(f"Mouse will be activated after {int(Mouse.INACTIVITY_TIMEOUT - time_since)} seconds")
                self._popup.label(message=f"Mouse will be activated after {int(Mouse.INACTIVITY_TIMEOUT - time_since)} seconds")
                self._popup.show()
            if time_since >= Mouse.INACTIVITY_TIMEOUT:
                self._popup.hide()
                self.stop_clicking.clear()
                log.info("[AUTO] No activity detected. Starting autoclick...")
                mouse.move(20, 1065)  # нижній лівий кут
                self.mouse_state = "ON"
                while not self.stop_clicking.is_set():
                    mouse.click('left')
                    time.sleep(Mouse.CLICK_INTERVAL)
                self.mouse_state = "OFF"
            else:
                time.sleep(1)
        self.detector_state = "OFF"
        self._cursor_detector_button.config(text=f"Detector-> {self.detector_state}")

    # +++  MANUAL ++++++++++++++++++++++++++++
    """
    Виключно ручне ввімкнення і виключно ручне вимкнення
    Вмикати і вимикати через кнопку Mouse Start/Stop
    """
    def _click(self):
        mouse.click()
        self._mouse_id = self.child_window.after(30000, self._click)

    # +++ Buttons and Other +++++++++++++++++++
    def on_button_stop(self):
        if self._mouse_id:
            self.child_window.after_cancel(self._mouse_id)
            self._mouse_id = None
            self.mouse_state = "OFF"
        else:
            self.mouse_state = "ON"
            mouse.move(20, 1065)
            self._click()
        self._mouse_stop_button.config(text=f"Mouse {self.mouse_state}")

    def on_button_detector(self):
        if self.detector_state == "OFF":
            self.detector_state = "ON"
            self._detector_flag = True
            self.last_activity = time.time()
            threading.Thread(target=self.activity_listener, daemon=True).start()
            threading.Thread(target=self.auto_clicker, daemon=True).start()
        else:
            self._detector_flag = False
            self.detector_state = "Waiting..."
        self._cursor_detector_button.config(text=f"Detector-> {self.detector_state}")

    @staticmethod
    def get_screen_size(direction):
        user32 = ctypes.windll.user32
        if direction == "x":
            return user32.GetSystemMetrics(0)
        elif direction == "y":
            return user32.GetSystemMetrics(1)
