# ui/title_bar.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint

class TitleBar(QWidget):
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.parent = parent
        self._pressed = False
        self._press = QPoint(0,0)
        self.setFixedHeight(46)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12,0,12,0)
        self.title = QLabel(title)
        layout.addWidget(self.title)
        layout.addStretch()

        self.min = QPushButton("—")
        self.max = QPushButton("▢")
        self.close = QPushButton("✕")
        for b in (self.min,self.max,self.close):
            b.setFixedSize(36,28)
        layout.addWidget(self.min); layout.addWidget(self.max); layout.addWidget(self.close)

        self.min.clicked.connect(self.parent.showMinimized)
        self.max.clicked.connect(lambda: self.parent.showNormal() if self.parent.isMaximized() else self.parent.showMaximized())
        self.close.clicked.connect(self.parent.close)

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton:
            self._pressed=True
            self._press=e.globalPosition().toPoint()
    def mouseMoveEvent(self,e):
        if self._pressed:
            delta=e.globalPosition().toPoint()-self._press
            self.parent.move(self.parent.pos()+delta)
            self._press=e.globalPosition().toPoint()
    def mouseReleaseEvent(self,e):
        self._pressed=False
