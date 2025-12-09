# ui/big_screen.py
import os

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QSpacerItem
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap


class BigScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIG SCREEN")
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(18)

        # Вопрос (крупный текст вверху)
        self.question_label = QLabel("")
        self.question_label.setObjectName("question_label")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )
        layout.addWidget(self.question_label)

        # Название раунда
        self.round_title = QLabel("Раунд 1")
        self.round_title.setObjectName("round_title")
        self.round_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.round_title)

        # Большой таймер
        self.timer_label = QLabel("--:--")
        self.timer_label.setObjectName("timer_label")
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

        # Картинка раунда (если есть)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setVisible(False)
        layout.addWidget(self.image_label)

        # Пустое пространство, чтобы таблица ушла к низу
        layout.addItem(QSpacerItem(
            0, 0,
            QSizePolicy.Minimum,
            QSizePolicy.Expanding
        ))

        # Карточка с таблицей команд внизу
        self.card = QWidget()
        self.card.setProperty("role", "card")
        cl = QVBoxLayout(self.card)
        cl.setContentsMargins(20, 16, 20, 16)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # фиксированная высота под ~6 жирных строк
        self.table.setFixedHeight(260)

        cl.addWidget(self.table)
        layout.addWidget(self.card)

        self.current_image = None

    # ====== публичные методы обновления ======

    @Slot(list)
    def update_scores(self, teams):
        """Обновление списка команд и очков (до 6 строк, крупные)."""
        self.table.setRowCount(len(teams))
        for i, t in enumerate(teams):
            name_item = QTableWidgetItem(t["name"])
            score_item = QTableWidgetItem(str(t["score"]))
            score_item.setTextAlignment(Qt.AlignCenter)

            # высокие строки для читаемости на расстоянии
            self.table.setRowHeight(i, 60)

            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, score_item)

    @Slot(str)
    def update_timer(self, text):
        self.timer_label.setText(text)

    @Slot(str)
    def set_round_title(self, text):
        self.round_title.setText(text)

    @Slot(str)
    def set_question(self, text):
        """Текст текущего вопроса в верхней части экрана."""
        self.question_label.setText(text)

    def set_round_image(self, path):
        self.current_image = path
        if not path or not os.path.exists(path):
            self.image_label.clear()
            self.image_label.setVisible(False)
            return

        pix = QPixmap(path)
        scaled = pix.scaled(
            self.width() * 0.6,
            self.height() * 0.35,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)
        self.image_label.setVisible(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image:
            self.set_round_image(self.current_image)
