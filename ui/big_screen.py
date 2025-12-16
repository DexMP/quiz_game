# ui/big_screen.py
import os

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFont

from ui.snow_overlay import SnowOverlay
from ui.background_widget import BackgroundWidget
from utils.paths import resource_path


class BigScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIG SCREEN")
        self.setMinimumSize(800, 600)

        self.current_image = None

        # наш контейнер с фоном
        self.central = BackgroundWidget()
        self.setCentralWidget(self.central)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setVisible(False)
        

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["", "Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)

        table_font = QFont()
        table_font.setPointSize(48)
        table_font.setBold(True)
        self.table.setFont(table_font)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.central.layout.addWidget(self.table)

        self.question_label = QLabel("")
        self.question_label.setVisible(False)
        self.timer_label = QLabel("--:--")
        self.timer_label.setVisible(False)

        self.snow = SnowOverlay(self)
        self.snow.setGeometry(self.rect())
        self.snow.raise_()

        # фон по умолчанию
        self.set_background("pic/background_xmas.jpg")

    # просто прокидываем в BackgroundWidget
    def set_background(self, path: str | None):
        if not path:
            self.central.set_background(None)
            return

        abs_path = resource_path(path)
        print("BG PATH:", abs_path, "exists:", os.path.exists(abs_path))

        if not os.path.exists(abs_path):
            self.central.set_background(None)
            return

        self.central.set_background(abs_path)


    @Slot(list)
    def update_scores(self, teams):
        self.table.setRowCount(len(teams))
        game_started = any(t["score"] > 0 for t in teams)

        medals = {0: "👑", 1: "🥈", 2: "🥉", 3: "🎖️", 4: "🐥" , 5: "🤡"}

        item_font = QFont()
        item_font.setPointSize(56)
        item_font.setBold(True)
        item_font.setWeight(QFont.ExtraBold)

        available_height = self.table.viewport().height()
        header_height = self.table.horizontalHeader().height()
        row_count = len(teams) if len(teams) > 0 else 1
        row_height = max(100, (available_height - header_height) // row_count)

        for i, t in enumerate(teams):
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            num_item.setFont(item_font)

            team_name = t["name"]
            if game_started and i in medals:
                team_name = f"{medals[i]} {team_name}"

            name_item = QTableWidgetItem(team_name)
            name_item.setFont(item_font)

            score_item = QTableWidgetItem(str(t["score"]))
            score_item.setTextAlignment(Qt.AlignCenter)
            score_item.setFont(item_font)

            self.table.setItem(i, 0, num_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, score_item)
            self.table.setRowHeight(i, row_height)

    @Slot(str)
    def update_timer(self, text):
        pass

    @Slot(str)
    def set_question(self, text):
        pass

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

        if self.table.rowCount() > 0:
            available_height = self.table.viewport().height()
            header_height = self.table.horizontalHeader().height()
            row_height = max(100, (available_height - header_height) // self.table.rowCount())
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, row_height)

    def wheelEvent(self, event):
        event.ignore()
