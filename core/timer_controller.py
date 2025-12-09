# core/timer_controller.py
from PySide6.QtCore import QTimer


class TimerController:
    def __init__(self):
        self.remaining = 0
        self.running = False
        self._qtimer = QTimer()
        self._qtimer.setInterval(1000)
        self._qtimer.timeout.connect(self._tick)
        self._tick_cb = None
        self._finished_cb = None

    def start(self, seconds, callback=None, finished=None):
        self.remaining = seconds
        self.running = True
        self._tick_cb = callback
        self._finished_cb = finished
        self._qtimer.start()
        if self._tick_cb:
            self._tick_cb()

    def toggle_pause(self):
        if self.running:
            self._qtimer.stop()
            self.running = False
        else:
            if self.remaining > 0:
                self._qtimer.start()
                self.running = True

    def reset(self):
        self._qtimer.stop()
        self.running = False
        self.remaining = 0

    def _tick(self):
        if self.remaining > 0:
            self.remaining -= 1
            if self._tick_cb:
                self._tick_cb()
            if self.remaining == 0:
                self._qtimer.stop()
                self.running = False
                if self._finished_cb:
                    self._finished_cb()

    def format_time(self, seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"
