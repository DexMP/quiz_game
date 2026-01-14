# ui/flash_effect.py
"""Эффект вспышки света на экране"""

from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget


class FlashEffect(QWidget):
    """Виджет для создания эффекта вспышки света"""
    
    def __init__(self, parent=None, duration: int = 300):
        """Инициализация эффекта вспышки
        
        Args:
            parent: Родительский виджет
            duration: Длительность вспышки в миллисекундах
        """
        super().__init__(parent)
        self.duration = duration
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        # Прозрачность для анимации
        self._opacity = 0.0
        self.setStyleSheet("background-color: rgba(255, 215, 0, 0);")  # Золотой цвет
        
        # Анимация для прозрачности
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.finished.connect(self.hide)
    
    def flash(self, color: QColor | None = None) -> None:
        """Создать вспышку
        
        Args:
            color: Цвет вспышки (по умолчанию золотой)
        """
        if color is None:
            color = QColor(255, 215, 0)  # Золотой
        
        # Устанавливаем стиль с цветом и полной прозрачностью
        self.setStyleSheet(f"background-color: {color.name()};")
        
        # Размер вспышки равен размеру родителя
        if self.parent():
            parent_rect = self.parent().rect()
            self.setGeometry(parent_rect)
        
        self.show()
        self.raise_()
        
        # Используем простую визуальную анимацию через стиль
        # За счёт быстрого скрытия виджета создаётся эффект вспышки
        from PySide6.QtCore import QTimer
        QTimer.singleShot(self.duration, self.hide)
