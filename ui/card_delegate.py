from PySide6.QtWidgets import QStyledItemDelegate, QApplication
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPalette
from PySide6.QtCore import Qt, QRect, QModelIndex, QSize

class CardDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 20
        self.leader_row = None
        self.changed_row = None

    def set_leader_row(self, row: int | None):
        self.leader_row = row
        if self.parent():
            self.parent().viewport().update()

    def set_changed_row(self, row: int | None):
        self.changed_row = row
        if self.parent():
            self.parent().viewport().update()

    def _get_theme_colors(self):
        """Получить цвета в зависимости от темы"""
        palette = QApplication.palette()
        is_dark = palette.color(QPalette.Window).lightness() < 128
        
        if is_dark:
            # Тёмная тема
            base_bg = QColor(45, 45, 48, 220)      # Тёмно-серый фон
            base_border = QColor(255, 255, 255, 25) # Светлая граница
            leader_bg = QColor(60, 55, 40, 230)     # Тёплый тёмный фон для лидера
            changed_bg = QColor(40, 50, 70, 235)    # Голубоватый тёмный фон
        else:
            # Светлая тема
            base_bg = QColor(255, 255, 255, 220)
            base_border = QColor(0, 0, 0, 25)
            leader_bg = QColor(252, 249, 228, 230)
            changed_bg = QColor(230, 238, 255, 235)
        
        return base_bg, base_border, leader_bg, changed_bg

    def paint(self, painter: QPainter, option, index: QModelIndex):
        rect: QRect = option.rect
        row = index.row()
        column = index.column()
        view = option.widget

        # Получаем цвета в зависимости от темы
        base_bg, base_border, leader_bg, changed_bg = self._get_theme_colors()
        bg_color = QColor(base_bg)
        border_color = QColor(base_border)

        # лидер — тёплый фон
        if self.leader_row is not None and row == self.leader_row:
            bg_color = QColor(leader_bg)

        # изменённая строка — мягкий голубой фон (без мигания)
        if self.changed_row is not None and row == self.changed_row:
            bg_color = QColor(changed_bg)

        if column == 0:
            row_rect = QRect(rect)
            model = view.model()
            for c in range(1, model.columnCount()):
                row_rect = row_rect.united(view.visualRect(model.index(row, c)))

            card_rect = QRect(
                row_rect.left() + 8,
                row_rect.top() + 6,
                row_rect.width() - 16,
                row_rect.height() - 12,
            )

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)

            shadow_rect = card_rect.translated(0, 3)
            painter.setBrush(QColor(0, 0, 0, 35))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(shadow_rect, self.radius, self.radius)

            painter.setBrush(QBrush(bg_color))
            painter.setPen(QPen(border_color, 1))
            painter.drawRoundedRect(card_rect, self.radius, self.radius)

            painter.restore()

        option2 = option
        if column == 0:
            option2.rect = option.rect.adjusted(18, 0, -8, 0)
        else:
            option2.rect = option.rect.adjusted(8, 0, -18, 0)

        super().paint(painter, option2, index)

    def sizeHint(self, option, index):
        base = super().sizeHint(option, index)
        return QSize(base.width(), base.height() + 16)
