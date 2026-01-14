# ui/confetti_overlay.py
import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath
from PySide6.QtWidgets import QWidget


class Confetti:
    """Класс для одного конфетти"""
    SHAPES = ['circle', 'square', 'triangle', 'rectangle']
    COLORS = [
        QColor(255, 77, 77),    # красный
        QColor(77, 166, 255),   # синий
        QColor(255, 195, 77),   # жёлтый
        QColor(119, 221, 119),  # зелёный
        QColor(186, 85, 211),   # фиолетовый
        QColor(255, 105, 180),  # розовый
        QColor(255, 140, 0),    # оранжевый
        QColor(72, 209, 204),   # бирюзовый
    ]
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # случайные параметры
        self.shape = random.choice(self.SHAPES)
        self.color = random.choice(self.COLORS)
        self.size = random.randint(6, 14)
        self.speed_y = random.uniform(2.0, 4.5)
        self.speed_x = random.uniform(-1.5, 1.5)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)
        self.swing_amplitude = random.uniform(0.5, 2.0)
        self.swing_speed = random.uniform(0.05, 0.15)
        self.swing_offset = random.uniform(0, math.pi * 2)
        
    def update(self):
        """Обновление позиции конфетти"""
        # падение вниз
        self.y += self.speed_y
        
        # качание из стороны в сторону (синусоида)
        self.x += self.speed_x + math.sin(self.y * self.swing_speed + self.swing_offset) * self.swing_amplitude
        
        # вращение
        self.rotation += self.rotation_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
            
        # если вышло за границы, сбрасываем наверх
        if self.y - self.size > self.height:
            self.y = random.randint(-self.height, 0)
            self.x = random.randint(0, self.width)
            
    def draw(self, painter: QPainter):
        """Отрисовка конфетти"""
        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.rotation)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        
        half = self.size / 2
        
        if self.shape == 'circle':
            painter.drawEllipse(QPointF(0, 0), half, half)
            
        elif self.shape == 'square':
            painter.drawRect(QRectF(-half, -half, self.size, self.size))
            
        elif self.shape == 'rectangle':
            w = self.size * 1.5
            h = self.size * 0.5
            painter.drawRect(QRectF(-w/2, -h/2, w, h))
            
        elif self.shape == 'triangle':
            path = QPainterPath()
            path.moveTo(0, -half)
            path.lineTo(half, half)
            path.lineTo(-half, half)
            path.closeSubpath()
            painter.drawPath(path)
            
        painter.restore()


class ConfettiOverlay(QWidget):
    """Оверлей с падающими конфетти для праздничного эффекта"""
    
    def __init__(self, parent=None, count=30):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.confetti_count = count
        self.confetti_list = []
        
        self._init_confetti()
        
        # таймер для анимации
        self.timer = QTimer(self)
        self.timer.setInterval(50)  # ~33 FPS
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        
    def _init_confetti(self):
        """Инициализация конфетти"""
        self.confetti_list = []
        w = max(self.width(), 1)
        h = max(self.height(), 1)
        
        for _ in range(self.confetti_count):
            x = random.randint(0, w)
            y = random.randint(-h, h)
            self.confetti_list.append(Confetti(x, y, w, h))
            
    def resizeEvent(self, event):
        """При изменении размера окна пересоздаём конфетти"""
        super().resizeEvent(event)
        self._init_confetti()
        
    def _tick(self):
        """Обновление позиций всех конфетти"""
        w = self.width()
        h = self.height()
        
        for conf in self.confetti_list:
            conf.width = w
            conf.height = h
            conf.update()
            
        self.update()  # перерисовка
        
    def paintEvent(self, event):
        """Отрисовка всех конфетти"""
        if not self.confetti_list:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        for conf in self.confetti_list:
            conf.draw(painter)
            
        painter.end()
