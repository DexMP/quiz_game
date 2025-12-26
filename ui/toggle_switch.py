from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QCheckBox, QApplication


class ToggleSwitch(QCheckBox):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(24)
        self._update_colors()

    def _update_colors(self):
        """Подбираем цвета под текущую тему по цвету окна."""
        bg = QApplication.palette().window().color()
        # очень простой детектор: светлая/тёмная тема по яркости
        brightness = (bg.red() + bg.green() + bg.blue()) / 3

        if brightness > 128:
            # светлая тема
            self._track_off = QColor("#E2E8F5")
            self._track_on = QColor("#2F80FF")
            self._thumb = QColor("#FFFFFF")
            self._border_off = QColor("#C4D6FF")
            self._border_on = QColor("#2F80FF")
        else:
            # тёмная тема
            self._track_off = QColor("#020617")
            self._track_on = QColor("#2381E9")
            self._thumb = QColor("#F9FAFB")
            self._border_off = QColor("#4B5563")
            self._border_on = QColor("#2381E9")

    def paintEvent(self, event):
        self._update_colors()

        radius = 10
        track_width = 38
        track_height = 20

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # геометрия трека
        track_rect = QRectF(0, (self.height() - track_height) / 2,
                            track_width, track_height)

        # цвета трека
        if self.isEnabled():
            track_color = self._track_on if self.isChecked() else self._track_off
            border_color = self._border_on if self.isChecked() else self._border_off
        else:
            track_color = QColor(track_color if (track_color := self._track_off) else "#E5E7EB")
            border_color = QColor("#D1D5DB")

        # трек
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_rect, radius, radius)

        # кружок
        margin = 2
        thumb_d = track_height - margin * 2
        if self.isChecked():
            cx = track_rect.right() - margin - thumb_d / 2
        else:
            cx = track_rect.left() + margin + thumb_d / 2
        cy = track_rect.center().y()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self._thumb if self.isEnabled() else QColor("#E5E7EB")))
        painter.drawEllipse(QPointF(cx, cy), thumb_d / 2, thumb_d / 2)

        # текст
        painter.setPen(self.palette().text().color())
        text_rect = QRectF(track_rect.right() + 8, 0,
                           self.width() - track_rect.right() - 8,
                           self.height())
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())

        painter.end()
