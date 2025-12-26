# ui/big_screen.py
import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFontDatabase, QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)

from ui.snow_overlay import SnowOverlay
from ui.background_widget import BackgroundWidget
from ui.card_delegate import CardDelegate
from utils.paths import resource_path


class BigScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BIG SCREEN")
        self.setMinimumSize(800, 600)

        self.current_image = None
        self._last_scores = {}
        self._changed_row = None

        # ----- шрифт Montserrat -----
        fonts_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
        regular_path = os.path.abspath(os.path.join(fonts_dir, "Montserrat-Regular.ttf"))
        bold_path = os.path.abspath(os.path.join(fonts_dir, "Montserrat-Bold.ttf"))

        for path in (regular_path, bold_path):
            if os.path.exists(path):
                QFontDatabase.addApplicationFont(path)

        families = (
            QFontDatabase.applicationFontFamilies(
                QFontDatabase.addApplicationFont(bold_path)
            )
            if os.path.exists(bold_path)
            else []
        )
        if families:
            montserrat = families[0]
        else:
            montserrat = "Montserrat"

        self.row_font = QFont(montserrat, 28, QFont.Medium)   # название команды
        self.score_font = QFont(montserrat, 34, QFont.Bold)   # очки, крупнее

        # ----- контейнер с фоном -----
        self.central = BackgroundWidget()
        self.setCentralWidget(self.central)

        # ----- таблица команд -----
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["", "Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        self.table.setShowGrid(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)

        # базовый шрифт таблицы (Montserrat)
        self.table.setFont(self.row_font)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # делегат-карточки
        self.card_delegate = CardDelegate(self.table)
        self.table.setItemDelegate(self.card_delegate)

        self.central.layout.addWidget(self.table)

        # скрытые элементы (для совместимости интерфейса)
        self.image_label = QLabel()
        self.image_label.setVisible(False)

        self.question_label = QLabel("")
        self.question_label.setVisible(False)
        self.timer_label = QLabel("--:--")
        self.timer_label.setVisible(False)

        # снежный оверлей
        self.snow = SnowOverlay(self)
        self.snow.setGeometry(self.rect())
        self.snow.raise_()

        # фон по умолчанию
        self.set_background("pic/background_xmas.jpg")

    # прокидываем фон в BackgroundWidget
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

        medals = {0: "👑", 1: "🥈", 2: "🥉", 3: "🎖️", 4: "🐥", 5: "🤡"}

        num_font = QFont(self.row_font)
        num_font.setPointSize(32)
        num_font.setBold(True)

        available_height = self.table.viewport().height()
        header_height = self.table.horizontalHeader().height()
        row_count = len(teams) if len(teams) > 0 else 1
        row_height = max(100, (available_height - header_height) // row_count)

        for i, t in enumerate(teams):
            # номер
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            num_item.setFont(num_font)

            # название команды с медалью
            team_name = t["name"]
            if game_started and i in medals:
                team_name = f"{medals[i]} {team_name}"

            name_item = QTableWidgetItem(team_name)
            name_item.setFont(self.row_font)

            # очки крупнее
            score_item = QTableWidgetItem(str(t["score"]))
            score_item.setTextAlignment(Qt.AlignCenter)
            score_item.setFont(self.score_font)

            self.table.setItem(i, 0, num_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, score_item)
            self.table.setRowHeight(i, row_height)

        # определить, какая строка изменилась
        old_scores = self._last_scores
        self._last_scores = {t["name"]: t["score"] for t in teams}
        changed_row = None
        for i, t in enumerate(teams):
            if old_scores.get(t["name"]) is not None and old_scores.get(t["name"]) != t["score"]:
                changed_row = i

        self._changed_row = changed_row
        self.card_delegate.set_leader_row(0 if teams else None)
        self.card_delegate.set_changed_row(changed_row)

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
            row_height = max(
                100, (available_height - header_height) // self.table.rowCount()
            )
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, row_height)

    def wheelEvent(self, event):
        event.ignore()
