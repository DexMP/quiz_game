import random
import math
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import (
    QColor, QPainter, QPen, QBrush, QPainterPath,
    QLinearGradient, QRadialGradient
)
from PySide6.QtWidgets import QWidget


def create_star_path(center_x, center_y, outer_radius, inner_radius=None) -> QPainterPath:
    """Вспомогательная функция для рисования звезды"""
    if inner_radius is None:
        inner_radius = outer_radius * 0.4

    path = QPainterPath()
    angle = -math.pi / 2
    angle_step = math.pi / 5

    path.moveTo(
        center_x + math.cos(angle) * outer_radius,
        center_y + math.sin(angle) * outer_radius
    )

    for i in range(1, 10):
        angle += angle_step
        r = inner_radius if i % 2 != 0 else outer_radius
        path.lineTo(
            center_x + math.cos(angle) * r,
            center_y + math.sin(angle) * r
        )
    path.closeSubpath()
    return path


class Tank:
    """Класс детализированного танка"""
    def __init__(self, screen_width, screen_height):
        # Размеры увеличим для детализации
        self.width = 120
        self.height = 65
        self.screen_height = screen_height
        
        self.x = -self.width
        # Ставим на "землю" с небольшим отступом
        self.y = self.screen_height - self.height - 15 
        
        self.speed = 2.5 # Чуть медленнее, чтобы разглядеть детали
        self.direction = 1 

        # Цвета
        self.color_dark = QColor(50, 65, 30)     # Темно-зеленый (тень)
        self.color_mid = QColor(85, 107, 47)     # Оливковый (база)
        self.color_light = QColor(120, 140, 80)  # Светло-оливковый (блик)
        self.tracks_color = QColor(40, 40, 40)   # Цвет резины/металла гусениц
        self.star_color = QColor(220, 20, 60)    # Красный
        
        # Анимация колес и антенны
        self.wheel_rotation = 0.0
        self.track_offset = 0.0
        self.antenna_sway = 0.0

    def update(self, screen_width, screen_height):
        """Обновление позиции и состояния анимации"""
        self.screen_height = screen_height
        self.y = self.screen_height - self.height - 15
        
        self.x += self.speed

        # Разворот
        if self.speed > 0 and self.x > screen_width + self.width * 0.2:
             self.speed = -abs(self.speed)
             self.direction = -1
        elif self.speed < 0 and self.x < -self.width * 1.2:
             self.speed = abs(self.speed)
             self.direction = 1
             
        # Анимация вращения колес и движения траков
        # Чем быстрее едем, тем быстрее крутятся
        rotation_speed = self.speed * 2 
        self.wheel_rotation += rotation_speed
        self.track_offset -= rotation_speed * 0.5 # Смещение текстуры гусеницы

        # Покачивание антенны (зависит от скорости)
        self.antenna_sway = math.sin(self.wheel_rotation * 0.1) * abs(self.speed) * 1.5

    def draw_wheels(self, painter, tracks_rect):
        """Рисует вращающиеся катки"""
        wheel_radius = tracks_rect.height() * 0.35
        num_wheels = 5
        spacing = (tracks_rect.width() - wheel_radius*2) / (num_wheels - 1)
        
        start_x = tracks_rect.left() + wheel_radius
        center_y = tracks_rect.center().y()

        painter.setPen(QPen(self.color_dark, 2))
        # Градиент для колеса, чтобы оно казалось объемным
        wheel_grad = QRadialGradient(0, 0, wheel_radius)
        wheel_grad.setColorAt(0.7, self.color_mid)
        wheel_grad.setColorAt(1.0, self.tracks_color)
        painter.setBrush(wheel_grad)

        for i in range(num_wheels):
            wx = start_x + i * spacing
            
            painter.save()
            painter.translate(wx, center_y)
            # Вращаем колесо
            painter.rotate(self.wheel_rotation)
            
            painter.drawEllipse(QPointF(0, 0), wheel_radius, wheel_radius)
            # Рисуем "спицы" или болты, чтобы было видно вращение
            painter.setPen(QPen(self.color_dark, 2))
            painter.drawLine(0, -wheel_radius*0.6, 0, wheel_radius*0.6)
            painter.drawLine(-wheel_radius*0.6, 0, wheel_radius*0.6, 0)
            
            painter.restore()

    def draw(self, painter: QPainter):
        """Детализированная отрисовка танка"""
        painter.save()
        painter.translate(self.x, self.y)
        
        # Зеркалирование при движении влево
        if self.direction == -1:
             painter.scale(-1, 1)
             painter.translate(-self.width, 0)

        # == ХОДОВАЯ ЧАСТЬ ==
        tracks_h = self.height * 0.35
        tracks_rect = QRectF(0, self.height - tracks_h, self.width, tracks_h)
        
        # 1. Сама гусеничная лента (фон)
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(self.tracks_color)
        painter.drawRoundedRect(tracks_rect, tracks_h/2, tracks_h/2)
        
        # 2. Текстура траков (насечки на гусенице)
        painter.save()
        painter.setClipRect(tracks_rect) # Рисуем только внутри гусеницы
        painter.setPen(QPen(QColor(20, 20, 20), 2))
        tread_spacing = 10
        # Рисуем линии с учетом смещения (track_offset) для анимации
        start_offset = self.track_offset % tread_spacing
        for i in range(int(self.width / tread_spacing) + 2):
            tx = i * tread_spacing + start_offset - tread_spacing
            painter.drawLine(tx, tracks_rect.top(), tx, tracks_rect.bottom())
        painter.restore()
        
        # 3. Вращающиеся катки
        self.draw_wheels(painter, tracks_rect)

        # == КОРПУС ==
        body_h = self.height * 0.4
        body_y = self.height - tracks_h - body_h + 5
        # Делаем корпус не прямоугольным, а с наклонным лбом
        body_path = QPainterPath()
        body_path.moveTo(10, body_y) # Верхний левый (корма)
        body_path.lineTo(self.width - 15, body_y) # Начало склона лба
        body_path.lineTo(self.width - 5, body_y + body_h * 0.5) # Нос
        body_path.lineTo(self.width - 10, body_y + body_h) # Низ носа
        body_path.lineTo(5, body_y + body_h) # Низ кормы
        body_path.closeSubpath()
        
        # Градиент для объема корпуса
        body_grad = QLinearGradient(0, body_y, 0, body_y + body_h)
        body_grad.setColorAt(0, self.color_light)
        body_grad.setColorAt(0.5, self.color_mid)
        body_grad.setColorAt(1, self.color_dark)
        
        painter.setPen(QPen(self.color_dark, 1))
        painter.setBrush(body_grad)
        painter.drawPath(body_path)
        
        # Детали корпуса: решетка МТО сзади
        painter.setBrush(self.color_dark)
        painter.drawRect(12, body_y + 5, 20, body_h * 0.6)
        # Детали корпуса: люк водителя спереди
        painter.drawRect(self.width - 35, body_y + 2, 15, 5)


        # == БАШНЯ ==
        turret_w = self.width * 0.55
        turret_h = self.height * 0.3
        turret_x = self.width * 0.2
        turret_y = body_y - turret_h + 5
        
        turret_rect = QRectF(turret_x, turret_y, turret_w, turret_h)

        # Градиент для башни
        turret_grad = QLinearGradient(0, turret_y, 0, turret_y + turret_h)
        turret_grad.setColorAt(0, self.color_light)
        turret_grad.setColorAt(1, self.color_mid)
        
        painter.setBrush(turret_grad)
        painter.drawRoundedRect(turret_rect, 15, 10)
        
        # Деталь: Командирская башенка (люк сверху)
        painter.setBrush(self.color_mid)
        painter.drawEllipse(turret_x + 10, turret_y - 5, 20, 10)
        
        # Деталь: Антенна (качается)
        antenna_base_x = turret_x + turret_w - 15
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(
            QPointF(antenna_base_x, turret_y), 
            QPointF(antenna_base_x + self.antenna_sway, turret_y - 30)
        )

        # == ДУЛО ==
        barrel_len = 45
        barrel_w = 8
        barrel_y = turret_y + turret_h/2 - barrel_w/2
        barrel_start_x = turret_x + turret_w - 10
        
        painter.setPen(QPen(self.color_dark, 1))
        painter.setBrush(self.color_mid)
        # Основная часть ствола
        painter.drawRect(barrel_start_x, barrel_y, barrel_len, barrel_w)
        
        # Деталь: Дульный тормоз на конце
        brake_w = 12
        brake_len = 10
        painter.setBrush(self.color_dark)
        painter.drawRect(barrel_start_x + barrel_len, barrel_y + barrel_w/2 - brake_w/2, brake_len, brake_w)

        # == ЗВЕЗДА НА БАШНЕ ==
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.star_color)
        # Рисуем чуть сбоку, чтобы не перекрывать люки
        star_path = create_star_path(turret_rect.center().x() + 5, turret_rect.center().y(), turret_h * 0.35)
        painter.drawPath(star_path)

        painter.restore()


class Parachute:
    """Класс для парашюта (без изменений, работает хорошо)"""
    COLORS = [
        QColor(85, 107, 47),    
        QColor(107, 142, 35),   
        QColor(139, 115, 85),   
        QColor(74, 93, 35),     
    ]
    STAR_COLOR = QColor(220, 20, 60) 
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.color = random.choice(self.COLORS)
        self.size = random.randint(40, 65)  
        self.speed_y = random.uniform(1.0, 2.2)
        self.speed_x = random.uniform(-0.3, 0.3)
        
        self.swing_amplitude = random.uniform(1.5, 3.5)
        self.swing_speed = random.uniform(0.015, 0.04)
        self.swing_offset = random.uniform(0, math.pi * 2)
        self.max_tilt = random.uniform(8, 15)
        self.rotation = 0
        
    def update(self):
        self.y += self.speed_y
        swing_phase = math.sin(self.y * self.swing_speed + self.swing_offset)
        self.x += self.speed_x + swing_phase * self.swing_amplitude
        self.rotation = swing_phase * self.max_tilt
            
        full_height = self.size * 2
        
        if self.y - full_height > self.height:
            top_bound = -max(self.height, int(full_height) + 10)
            bottom_bound = -int(full_height)
            self.y = random.randint(top_bound, bottom_bound)
            self.x = random.randint(0, self.width)
            
    def draw(self, painter: QPainter):
        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.rotation)
        
        w = self.size
        h = self.size
        
        painter.setPen(QPen(QColor(40, 40, 40), 1.2))
        painter.drawLine(QPointF(-w*0.4, 0), QPointF(0, h))
        painter.drawLine(QPointF(w*0.4, 0), QPointF(0, h))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawPie(QRectF(-w/2, -h/2, w, h), 0, 180 * 16)

        painter.setBrush(self.STAR_COLOR)
        canopy_star = create_star_path(0, -h*0.2, w * 0.15)
        painter.drawPath(canopy_star)
        
        box_w = w * 0.35
        box_h = w * 0.35
        box_rect = QRectF(-box_w/2, h, box_w, box_h)
        painter.setBrush(QBrush(QColor(101, 67, 33)))
        painter.drawRect(box_rect)

        painter.setBrush(self.STAR_COLOR)
        box_star = create_star_path(box_rect.center().x(), box_rect.center().y(), box_w * 0.25)
        painter.drawPath(box_star)
        
        painter.restore()


class ConfettiOverlay(QWidget):
    """Оверлей с парашютами и детализированным танком"""
    def __init__(self, parent=None, count=18): 
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.confetti_count = count
        self.confetti_list = []

        self.tank = Tank(self.width(), self.height())
        
        self._init_confetti()
        
        self.timer = QTimer(self)
        self.timer.setInterval(35) # Чуть увеличим FPS для плавности колес
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        
    def _init_confetti(self):
        self.confetti_list = []
        w = max(self.width(), 1)
        h = max(self.height(), 50) 
        
        for _ in range(self.confetti_count):
            x = random.randint(0, w)
            y = random.randint(-h * 2, h) 
            self.confetti_list.append(Parachute(x, y, w, h))
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._init_confetti()
        w = self.width()
        h = self.height()
        if hasattr(self, 'tank'):
             self.tank.update(w, h)
        
    def _tick(self):
        w = self.width()
        h = self.height()
        for conf in self.confetti_list:
            conf.update()
        self.tank.update(w, h)
        self.update() 
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.tank.draw(painter)
        for conf in self.confetti_list:
            conf.draw(painter)
        painter.end()