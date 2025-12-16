# ui/background_widget.py
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_pixmap = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(0)

    def set_background(self, path: str | None):
        if not path:
            self._bg_pixmap = None
            self.update()
            return

        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            print("BACKGROUND NOT FOUND:", abs_path)
            self._bg_pixmap = None
        else:
            pix = QPixmap(abs_path)
            if pix.isNull():
                print("BACKGROUND LOAD FAILED:", abs_path)
                self._bg_pixmap = None
            else:
                self._bg_pixmap = pix
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._bg_pixmap:
            return

        painter = QPainter(self)
        rect = self.rect()
        scaled = self._bg_pixmap.scaled(
            rect.size(),
            Qt.KeepAspectRatioByExpanding,  # эффект cover
            Qt.SmoothTransformation,
        )
        x = (rect.width() - scaled.width()) // 2
        y = (rect.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
