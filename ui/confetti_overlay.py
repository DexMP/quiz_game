import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath, QRadialGradient
from PySide6.QtWidgets import QWidget


def create_petal_path(size) -> QPainterPath:
    """Создает контур лепестка розы"""
    path = QPainterPath()
    path.moveTo(0, -size)
    path.cubicTo(size * 0.8, -size * 0.8, size * 0.9, size * 0.4, 0, size * 0.8)
    path.cubicTo(-size * 0.9, size * 0.4, -size * 0.8, -size * 0.8, 0, -size)
    return path


class Petal:
    """Класс для падающего лепестка розы"""
    COLORS = [
        QColor(220, 20, 60),   
        QColor(255, 105, 180), 
        QColor(255, 192, 203), 
        QColor(255, 0, 0),     
        QColor(255, 240, 245), 
    ]
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.color = random.choice(self.COLORS)
        self.size = random.uniform(10, 25)
        self.speed_y = random.uniform(1.5, 3.5)
        self.speed_x = random.uniform(-1.0, 1.0)
        
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        self.flip_phase = random.uniform(0, math.pi * 2)
        self.flip_speed = random.uniform(0.05, 0.15)
        
        self.swing_offset = random.uniform(0, math.pi * 2)
        self.swing_speed = random.uniform(0.02, 0.05)
        self.swing_amplitude = random.uniform(1.0, 3.0)
        
    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x + math.sin(self.y * self.swing_speed + self.swing_offset) * self.swing_amplitude
        
        self.rotation += self.rotation_speed
        self.flip_phase += self.flip_speed
            
        if self.y - self.size > self.height:
            top_bound = -max(self.height, int(self.size) + 10)
            bottom_bound = -int(self.size)
            self.y = random.randint(top_bound, bottom_bound)
            self.x = random.randint(0, self.width)
            
    def draw(self, painter: QPainter):
        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.rotation)
        
        scale_y = math.cos(self.flip_phase)
        painter.scale(1, scale_y)
        
        painter.setPen(Qt.NoPen)
        grad = QRadialGradient(0, 0, self.size)
        grad.setColorAt(0, self.color.lighter(120))
        grad.setColorAt(1, self.color.darker(110))
        painter.setBrush(grad)
        
        petal_path = create_petal_path(self.size)
        painter.drawPath(petal_path)
        painter.restore()


class ConfettiOverlay(QWidget):
    """Оверлей только с падающими лепестками роз"""
    def __init__(self, parent=None, count=50): # Чуть увеличил количество лепестков для компенсации
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.petal_count = count
        self.petals = []
        
        self._init_scene()
        
        self.timer = QTimer(self)
        self.timer.setInterval(33) 
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        
    def _init_scene(self):
        self.petals = []
        w = max(self.width(), 1)
        h = max(self.height(), 50)
        
        for _ in range(self.petal_count):
            x = random.randint(0, w)
            top_bound = -max(h * 2, 100)
            self.petals.append(Petal(x, random.randint(top_bound, -10), w, h))
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._init_scene()
        
    def _tick(self):
        w = self.width()
        h = self.height()
        
        for petal in self.petals:
            petal.width = w
            petal.height = h
            petal.update()
            
        self.update() 
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        for petal in self.petals:
            petal.draw(painter)
            
        painter.end()