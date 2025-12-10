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
    QSpacerItem,
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFont

from ui.snow_overlay import SnowOverlay


class BigScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIG SCREEN")
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(18)

        # Вопрос
        self.question_label = QLabel("")
        self.question_label.setObjectName("question_label")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )
        layout.addWidget(self.question_label)

        # Таймер
        self.timer_label = QLabel("--:--")
        self.timer_label.setObjectName("timer_label")
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

        # Картинка раунда
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setVisible(False)
        layout.addWidget(self.image_label)

        # Спейсер, чтобы таблица была снизу
        layout.addStretch()

        # Карточка с таблицей команд
        self.card = QWidget()
        self.card.setProperty("role", "card")
        cl = QVBoxLayout(self.card)
        cl.setContentsMargins(16, 10, 16, 10)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["", "Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)

        # фиксированная высота строк и таблицы
        self.row_height = 110
        self.max_rows = 6

        table_font = QFont()
        table_font.setPointSize(24)
        table_font.setBold(True)
        self.table.setFont(table_font)

        # Устанавливаем высоту строк
        for i in range(self.max_rows):
            self.table.setRowHeight(i, self.row_height)

        # Рассчитываем и устанавливаем фиксированную высоту таблицы
        header_height = self.table.horizontalHeader().height()
        total_table_height = header_height + (self.max_rows * self.row_height) + 4  # +4 на borders
        self.table.setFixedHeight(total_table_height)
        
        # Фиксируем высоту карточки
        self.card.setFixedHeight(total_table_height + 20)  # +20 на отступы карточки

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        cl.addWidget(self.table)
        layout.addWidget(self.card)

        self.current_image = None

        # снежный оверлей
        self.snow = SnowOverlay(self)
        self.snow.setGeometry(self.rect())
        self.snow.raise_()

    @Slot(list)
    def update_scores(self, teams):
        self.table.setRowCount(len(teams))
        for i, t in enumerate(teams):
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)

            name_item = QTableWidgetItem(t["name"])
            score_item = QTableWidgetItem(str(t["score"]))
            score_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(i, 0, num_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, score_item)
            self.table.setRowHeight(i, self.row_height)


    @Slot(str)
    def update_timer(self, text):
        self.timer_label.setText(text)

    @Slot(str)
    def set_question(self, text):
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
        self.snow.setGeometry(self.rect())
        if self.current_image:
            self.set_round_image(self.current_image)
