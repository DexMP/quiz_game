# ui/snow_overlay.py
import random
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class SnowOverlay(QWidget):
    def __init__(self, parent=None, flakes=40):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.flakes = []
        self.flakes_count = flakes

        self._init_flakes()

        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    def _init_flakes(self):
        self.flakes = []
        w = max(self.width(), 1)
        h = max(self.height(), 1)
        for _ in range(self.flakes_count):
            x = random.randint(0, w)
            y = random.randint(-h, 0)
            r = random.randint(3, 6)
            speed = random.uniform(1.0, 2.5)
            drift = random.uniform(-0.6, 0.6)
            self.flakes.append([x, y, r, speed, drift])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._init_flakes()

    def _tick(self):
        w = self.width()
        h = self.height()
        for f in self.flakes:
            f[0] += f[4]
            f[1] += f[3]
            if f[1] - f[2] > h:
                f[0] = random.randint(0, w)
                f[1] = random.randint(-h, 0)
        self.update()

    def paintEvent(self, event):
        if not self.flakes:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        color = QColor(255, 255, 255, 190)
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        for x, y, r, *_ in self.flakes:
            p.drawEllipse(QPoint(int(x), int(y)), r, r)
        p.end()
