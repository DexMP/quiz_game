# ui/card_delegate.py
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRect, QModelIndex, QSize


class CardDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 20
        self.bg_color = QColor(255, 255, 255, 210)
        self.border_color = QColor(0, 0, 0, 25)

    def paint(self, painter: QPainter, option, index: QModelIndex):
        rect: QRect = option.rect
        row = index.row()
        column = index.column()
        view = option.widget  # QTableView/QTableWidget

        # считаем общую область строки по всем колонкам
        if column == 0:
            # первая колонка: рисуем карточку на всю строку
            row_rect = QRect(rect)
            for c in range(1, view.model().columnCount()):
                row_rect = row_rect.united(view.visualRect(view.model().index(row, c)))

            card_rect = QRect(
                row_rect.left() + 8,
                row_rect.top() + 4,
                row_rect.width() - 16,
                row_rect.height() - 8,
            )

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)

            shadow_rect = card_rect.translated(0, 2)
            painter.setBrush(QColor(0, 0, 0, 40))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(shadow_rect, self.radius, self.radius)

            painter.setBrush(QBrush(self.bg_color))
            painter.setPen(QPen(self.border_color, 1))
            painter.drawRoundedRect(card_rect, self.radius, self.radius)

            painter.restore()

        # смещаем текст внутри карточки
        option2 = option

        # слева чуть меньше отступ, чтобы номер влезал
        if column == 0:
            option2.rect = option.rect.adjusted(18, 0, -8, 0)
        else:
            option2.rect = option.rect.adjusted(8, 0, -18, 0)

        super().paint(painter, option2, index)

    def sizeHint(self, option, index):
        base = super().sizeHint(option, index)
        return QSize(base.width(), base.height() + 16)
