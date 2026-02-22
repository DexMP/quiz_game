# ui/big_screen.py
"""Большой экран для показа на проекторе/телевизоре"""

import os
from functools import lru_cache
from typing import List, Optional

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QFontDatabase, QFont, QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)

from core.team import Team
from ui.confetti_overlay import ConfettiOverlay
from ui.background_widget import BackgroundWidget
from ui.card_delegate import CardDelegate
from utils.paths import resource_path


class BigScreenWindow(QMainWindow):
    """Окно большого экрана для показа команд на проекторе"""
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BIG SCREEN")
        self.setMinimumSize(800, 600)

        self.current_image: Optional[str] = None
        self._last_scores: dict[str, int] = {}
        self._changed_row: Optional[int] = None

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
        montserrat = families[0] if families else "Montserrat"

        self.row_font: QFont = QFont(montserrat, 28, QFont.Medium)
        self.score_font: QFont = QFont(montserrat, 34, QFont.Bold)

        # ----- контейнер с фоном -----
        self.central = BackgroundWidget()
        self.setCentralWidget(self.central)

        # ----- таблица команд -----
        self.table: QTableWidget = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["", "Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.horizontalHeader().resizeSection(2, 180)
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

        self.table.setFont(self.row_font)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.card_delegate: CardDelegate = CardDelegate(self.table)
        self.table.setItemDelegate(self.card_delegate)

        self.central.layout.addWidget(self.table)

        # скрытые элементы (для совместимости интерфейса)
        self.image_label: QLabel = QLabel()
        self.image_label.setVisible(False)

        self.question_label: QLabel = QLabel("")
        self.question_label.setVisible(False)
        
        self.timer_label: QLabel = QLabel("--:--")
        self.timer_label.setVisible(False)

        # конфетти оверлей
        self.confetti: ConfettiOverlay = ConfettiOverlay(self)
        self.confetti.setGeometry(self.rect())
        self.confetti.raise_()

        from ui.flash_effect import FlashEffect

        # Создать эффект вспышки
        self.flash_effect: FlashEffect = FlashEffect(self, duration=300)
        self.flash_effect.hide()

        # фон по умолчанию
        self.set_background("pic/23_back.jpg")

    def set_background(self, path: Optional[str]) -> None:
        """Установить фоновое изображение
        
        Args:
            path: Путь к изображению или None для удаления фона
        """
        if not path:
            self.central.set_background(None)
            return

        abs_path = resource_path(path)
        print("BG PATH:", abs_path, "exists:", os.path.exists(abs_path))

        if not os.path.exists(abs_path):
            self.central.set_background(None)
            return

        self.central.set_background(abs_path)

    @staticmethod
    @lru_cache(maxsize=10)
    def _get_font_size_for_digits(digit_count: int) -> int:
        """Получить размер шрифта в зависимости от количества цифр
        
        Кэшируется для оптимизации производительности.
        
        Args:
            digit_count: Количество цифр в числе
            
        Returns:
            Размер шрифта в пунктах
        """
        if digit_count <= 2:
            return 34  # 0-99
        elif digit_count == 3:
            return 30  # 100-999
        elif digit_count == 4:
            return 26  # 1000-9999
        else:
            return 22  # 10000+

    def _get_adaptive_score_font(self, length: int) -> QFont:
        """Получить шрифт в зависимости от кол-ва символов (включая точки)"""
        font = QFont(self.score_font)
        
        if length <= 2:
            size = 34
        elif length == 3:
            size = 30
        elif length == 4:
            size = 26
        else:
            size = 22
            
        font.setPointSize(size)
        return font

    @Slot(list)
    def update_scores(self, teams: List[Team]) -> None:
        """Обновить таблицу очков с поддержкой дробных чисел"""
        self.table.setRowCount(len(teams))
        # Проверяем старт игры (учитываем float)
        game_started: bool = any(t.score > 0 for t in teams)

        medals: dict[int, str] = {
            0: "👑", 1: "🥈", 2: "🥉", 3: "🎖️", 4: "🐥", 5: "🤡"
        }

        num_font: QFont = QFont(self.row_font)
        num_font.setPointSize(32)
        num_font.setBold(True)

        available_height: int = self.table.viewport().height()
        header_height: int = self.table.horizontalHeader().height()
        row_count: int = len(teams) if len(teams) > 0 else 1
        row_height: int = max(100, (available_height - header_height) // row_count)

        for i, t in enumerate(teams):
            # 1. Номер команды
            num_item: QTableWidgetItem = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            num_item.setFont(num_font)

            # 2. Название команды с медалью
            team_name: str = t.name
            if game_started and i in medals:
                team_name = f"{medals[i]} {team_name}"

            name_item: QTableWidgetItem = QTableWidgetItem(team_name)
            name_item.setFont(self.row_font)

            # 3. Очки (ГЛАВНОЕ ИЗМЕНЕНИЕ)
            # Формат :g убирает лишние нули (.0), round гарантирует точность до десятых
            score_str = f"{round(t.score, 1):g}"
            score_item: QTableWidgetItem = QTableWidgetItem(score_str)
            score_item.setTextAlignment(Qt.AlignCenter)
            
            # Передаем длину строки для адаптации размера шрифта
            # (так как "10.5" длиннее чем "10", шрифт должен подстроиться)
            score_item.setFont(self._get_adaptive_score_font(len(score_str)))

            self.table.setItem(i, 0, num_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, score_item)
            self.table.setRowHeight(i, row_height)

        # Логика определения изменений для эффектов
        old_scores: dict[str, float] = self._last_scores
        self._last_scores = {t.name: t.score for t in teams}
        changed_row: Optional[int] = None
        
        for i, t in enumerate(teams):
            if t.name in old_scores and old_scores[t.name] != t.score:
                changed_row = i

        self._changed_row = changed_row
        
        # Эффект смены лидера
        if teams:
            current_leader = teams[0].name
            if not hasattr(self, '_prev_leader') or self._prev_leader != current_leader:
                if game_started: # Вспышка только если игра реально идет
                    self.flash_effect.flash(QColor(255, 215, 0)) 
                self._prev_leader = current_leader
        
        self.card_delegate.set_leader_row(0 if teams else None)
        self.card_delegate.set_changed_row(changed_row)

    @Slot(str)
    def update_timer(self, text: str) -> None:
        """Обновить текст таймера
        
        Args:
            text: Текст для отображения
        """
        pass

    @Slot(str)
    def set_question(self, text: str) -> None:
        """Установить текст вопроса
        
        Args:
            text: Текст вопроса
        """
        pass

    def set_round_image(self, path: Optional[str]) -> None:
        """Установить изображение раунда
        
        Args:
            path: Путь к изображению или None
        """
        self.current_image = path
        if not path or not os.path.exists(path):
            self.image_label.clear()
            self.image_label.setVisible(False)
            return
        pix = QPixmap(path)
        scaled = pix.scaled(
            self.width() * 60 // 100,
            self.height() * 35 // 100,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)
        self.image_label.setVisible(True)

    def resizeEvent(self, event) -> None:
        """Обработка изменения размера окна"""
        super().resizeEvent(event)
        self.confetti.setGeometry(self.rect())
        if self.current_image:
            self.set_round_image(self.current_image)

        if self.table.rowCount() > 0:
            available_height: int = self.table.viewport().height()
            header_height: int = self.table.horizontalHeader().height()
            row_height: int = max(
                100, (available_height - header_height) // self.table.rowCount()
            )
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, row_height)

    def wheelEvent(self, event) -> None:
        """Игнорировать колесо мыши"""
        event.ignore()
