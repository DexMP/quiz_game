# ui/main_window.py
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpinBox,
    QGroupBox,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QMenu,
    QCheckBox,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

# Кастоммная красота
from ui.big_screen import BigScreenWindow
from ui.dialogs import MonitorChoiceDialog, ask_team_name
from ui.toggle_switch import ToggleSwitch

# Стили
from assets.styles import AURORA_LIGHT_PRO, AURORA_DARK

# Логика
from core.team_manager import TeamManager
from core.timer_controller import TimerController
from core.theme_manager import ThemeManager
from core.state_manager import StateManager
from core.logger import Logger
from core.update_checker import fetch_latest_release
from core.version import APP_VERSION, is_update_available

APP_STATE = "quiz_state.json"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Самый умный родственник")
        self.resize(1200, 760)

        # core
        self.tm = TeamManager()
        self.timer = TimerController()
        self.th = ThemeManager()
        self.sm = StateManager()
        self.lg = Logger()

        # ui
        central = QWidget()
        self.setCentralWidget(central)
        ol = QVBoxLayout(central)
        ol.setContentsMargins(16, 12, 16, 12)
        ol.setSpacing(10)

        body = QHBoxLayout()
        ol.addLayout(body)

        # левая колонка — команды и история
        left_col = QVBoxLayout()
        teams_box = QGroupBox("Команды")
        tb_layout = QVBoxLayout(teams_box)
        top_row = QHBoxLayout()
        self.btn_add = QPushButton("Добавить команду")
        self.btn_remove = QPushButton("Удалить")
        self.btn_add.setObjectName("btn_add")
        self.btn_remove.setObjectName("btn_remove")
        top_row.addWidget(self.btn_add)
        top_row.addWidget(self.btn_remove)
        top_row.addStretch()
        tb_layout.addLayout(top_row)

        # таблица команд (2 колонки: Команда, Очки)
        self.table_card = QWidget()
        self.table_card.setProperty("role", "card")
        card_layout = QVBoxLayout(self.table_card)
        card_layout.setContentsMargins(6, 6, 6, 6)
        self.table = QTableWidget(0, 2)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setObjectName("adminTable")
        self.table.setHorizontalHeaderLabels(["Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        card_layout.addWidget(self.table)
        tb_layout.addWidget(self.table_card)
        left_col.addWidget(teams_box, 3)

        hist_box = QGroupBox("История")
        hb_layout = QVBoxLayout()
        self.hist = QPlainTextEdit()
        self.hist.setReadOnly(True)
        hb_layout.addWidget(self.hist)
        hist_box.setLayout(hb_layout)
        left_col.addWidget(hist_box, 1)

        body.addLayout(left_col, 3)

        # правая колонка — только большой экран и настройки
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        # Большой экран
        screen_box = QGroupBox("Большой экран")
        screen_layout = QVBoxLayout()

        row = QHBoxLayout()
        self.btn_show_big = QPushButton("Показать большой экран")
        self.btn_show_big.setObjectName("btn_primary")
        self.btn_close_big = QPushButton("Закрыть")
        self.btn_close_big.setObjectName("btn_close_big")
        self.btn_show_big.setMinimumHeight(40)
        self.btn_close_big.setMinimumHeight(40)

        row.addWidget(self.btn_show_big)
        row.addWidget(self.btn_close_big)
        screen_layout.addLayout(row)

        screen_box.setLayout(screen_layout)
        right_col.addWidget(screen_box)

        # Настройки
        settings_box = QGroupBox("Настройки")
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(8)

        io_row1 = QHBoxLayout()
        io_row1.setSpacing(8)
        self.btn_save = QPushButton("Сохранить")
        self.btn_load = QPushButton("Загрузить")
        for b in (self.btn_save, self.btn_load):
            b.setMinimumHeight(40)
            b.setMinimumWidth(120)
        io_row1.addWidget(self.btn_save)
        io_row1.addWidget(self.btn_load)
        settings_layout.addLayout(io_row1)

        self.btn_check_update = QPushButton(f"Проверить обновление\n(v{APP_VERSION})")
        self.btn_check_update.setMinimumHeight(46)
        self.btn_check_update.setMinimumWidth(260)
        settings_layout.addWidget(self.btn_check_update)

        # маленькая красная точка-индикатор обновления поверх кнопки
        from PySide6.QtWidgets import QLabel as _QLabelForBadge
        self.lbl_update_badge = _QLabelForBadge(self.btn_check_update)
        self.lbl_update_badge.setObjectName("lbl_update_badge")
        self.lbl_update_badge.setFixedSize(10, 10)
        self.lbl_update_badge.setVisible(False)
        self.lbl_update_badge.raise_()

        settings_box.setLayout(settings_layout)
        right_col.addWidget(settings_box)

        right_col.addStretch()
        body.addLayout(right_col, 2)

        from PySide6.QtWidgets import QCheckBox  # если где-то ещё нужен

        toggles_box = QGroupBox("Режимы")
        toggles_layout = QVBoxLayout()

        self.chk_dark = ToggleSwitch("Тёмная тема")
        self.chk_fullscreen = ToggleSwitch("Полноэкранный режим админки")
        self.chk_cloud = ToggleSwitch("Сохранение в облако (скоро)")
        self.chk_cloud.setEnabled(False)

        toggles_layout.addWidget(self.chk_dark)
        toggles_layout.addWidget(self.chk_fullscreen)
        toggles_layout.addWidget(self.chk_cloud)
        toggles_box.setLayout(toggles_layout)

        right_col.addWidget(toggles_box)

        # big screen
        self.big = BigScreenWindow()

        # состояние
        self.big_screen_index = None

        # флаг наличия обновления
        self._has_update = False

        # сигналы
        self.btn_add.clicked.connect(self.add_team)
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_show_big.clicked.connect(self.show_big)
        self.btn_save.clicked.connect(self.save_state)
        self.btn_load.clicked.connect(self.load_state_dialog)
        self.btn_check_update.clicked.connect(self.check_update)
        self.btn_show_big.clicked.connect(self.show_big)
        self.btn_close_big.clicked.connect(self.close_big)
        self.chk_dark.toggled.connect(self.toggle_theme_checkbox)
        self.chk_fullscreen.toggled.connect(self.toggle_admin_fullscreen)

        # периодический рефреш
        self.ui_timer = QTimer(self)
        self.ui_timer.setInterval(600)
        self.ui_timer.timeout.connect(self.refresh)
        self.ui_timer.start()

        # пробуем загрузить состояние
        if os.path.exists(APP_STATE):
            try:
                self.load_state(APP_STATE)
            except Exception:
                pass

        # позиционируем бейдж
        self.position_update_badge()

        # тихая проверка обновления при старте
        self.check_update_silent()

    # -------- переопределения --------

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.position_update_badge()

    def position_update_badge(self):
        if not hasattr(self, "lbl_update_badge") or not self.lbl_update_badge:
            return
        if not hasattr(self, "btn_check_update") or not self.btn_check_update:
            return
        bw = self.btn_check_update.width()
        w = self.lbl_update_badge.width()
        # правый верхний угол с небольшими отступами
        x = bw - w - 6
        y = 6
        self.lbl_update_badge.move(x, y)

    # -------- команды и таблица --------

    def add_team(self):
        name = ask_team_name(self)
        if not name:
            return
        self.tm.add_team(name)
        self.lg.log(f"Добавлена команда: {name}")
        self.refresh()

    def remove_selected(self):
        rows = sorted({i.row() for i in self.table.selectedIndexes()}, reverse=True)
        if not rows:
            QMessageBox.information(
                self, "Удаление", "Выберите хотя бы одну команду."
            )
            return
        
        # Получаем имена команд из выбранных строк (учитываем сортировку)
        sorted_teams = self.tm.get_sorted()
        teams_to_remove = []
        for r in rows:
            if r < len(sorted_teams):
                teams_to_remove.append(sorted_teams[r].name)  # ← ИЗМЕНЕНО: было ["name"]
        
        # Удаляем команды по именам
        for name in teams_to_remove:
            for idx, team in enumerate(self.tm.teams):
                if team.name == name:  # ← ИЗМЕНЕНО: было ["name"]
                    self.tm.remove_by_index(idx)
                    break
        
        self.lg.log("Удалены команды")
        self.refresh()

    
    def open_menu(self, pos):
        row = self.table.indexAt(pos).row()
        if row < 0:
            return
        
        # Получаем имя команды из отсортированного списка
        sorted_teams = self.tm.get_sorted()
        if row >= len(sorted_teams):
            return
        
        team_name = sorted_teams[row].name  # ← ИЗМЕНЕНО: было ["name"]
        
        # Находим индекс в оригинальном списке
        original_idx = None
        for idx, team in enumerate(self.tm.teams):
            if team.name == team_name:  # ← ИЗМЕНЕНО: было ["name"]
                original_idx = idx
                break
        
        if original_idx is None:
            return
        
        m = QMenu(self)
        for txt, val in [("+1", 1), ("+5", 5), ("-1", -1), ("-5", -5)]:
            act = QAction(txt, self)
            act.triggered.connect(
                lambda _, v=val, i=original_idx: self.tm.adjust(i, v)
            )
            m.addAction(act)
        m.exec(self.table.viewport().mapToGlobal(pos))
        self.refresh()


    def refresh(self):
        # Используем отсортированный список команд
        sorted_teams = self.tm.get_sorted()
        self.table.setRowCount(len(sorted_teams))

        for i, t in enumerate(sorted_teams):
            # Название команды
            name_item = QTableWidgetItem(t.name)
            self.table.setItem(i, 0, name_item)

            # Очки
            score_item = QTableWidgetItem(str(t.score))
            score_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, score_item)

            self.table.setRowHeight(i, 54)

        self.hist.setPlainText(self.lg.get_text())
        self.big.update_scores(sorted_teams)

    # -------- big screen --------

    def show_big(self):
        if self.big_screen_index is None:
            dlg = MonitorChoiceDialog(self)
            if dlg.exec() != 1:
                return
            idx = dlg.selected_index()
            if idx is None:
                return
            self.big_screen_index = idx
        idx = self.big_screen_index
        scr = QApplication.screens()[idx].geometry()
        self.big.setGeometry(scr)
        self.big.showFullScreen()

    def close_big(self):
        if self.big.isVisible():
            self.big.close()

    # -------- состояние --------

    def save_state(self):
        state = self.sm.build_state(
            self.tm,
            self.lg,
            self.th,
            self.timer,
            "",
        )
        try:
            self.sm.save(APP_STATE, state)
            self.lg.log("Состояние сохранено")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_state(self, path):
        data = self.sm.load(path)
        self.tm.load_from(data.get("teams", []))
        self.lg.load_from(data.get("history", []))

        remaining = data.get("remaining")
        if isinstance(remaining, int) and remaining >= 0:
            self.timer.remaining = remaining

        theme = data.get("theme")
        if theme:
            self.th.apply(theme)

        self.apply_theme_from_state()
        self.refresh()

    def load_state_dialog(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Загрузить состояние", "", "JSON files (*.json)"
        )
        if p:
            self.load_state(p)

    # -------- тема --------

    def apply_theme_from_state(self):
        mode = self.th.get().get("mode", "light")
        app = QApplication.instance()
        if mode == "dark":
            app.setStyleSheet(AURORA_DARK)
            self.chk_dark.setChecked(True)
        else:
            app.setStyleSheet(AURORA_LIGHT_PRO)
            self.chk_dark.setChecked(False)

    def toggle_theme(self):
        self.th.toggle_mode()
        self.apply_theme_from_state()

    # -------- Настройки переключателями --------
    def toggle_theme_checkbox(self, checked: bool):
        mode = "dark" if checked else "light"
        self.th.apply({"mode": mode})
        self.apply_theme_from_state()

    def toggle_admin_fullscreen(self, checked: bool):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    # -------- обновление --------

    def check_update_silent(self):
        try:
            self._has_update = is_update_available()
        except Exception:
            self._has_update = False
        self.update_update_indicator()

    def update_update_indicator(self):
        self.lbl_update_badge.setVisible(bool(self._has_update))

    def check_update(self):
        try:
            info = fetch_latest_release()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Проверка обновлений",
                f"Не удалось проверить обновление:\n{e}",
            )
            self._has_update = False
            self.update_update_indicator()
            return

        self._has_update = bool(info and info.has_update)
        self.update_update_indicator()

        if info.has_update:
            msg = QMessageBox(self)
            msg.setWindowTitle("Доступно обновление")
            msg.setText(
                f"Текущая версия: {info.current}\nНовая версия: {info.latest}"
            )
            msg.setInformativeText("Открыть страницу релиза в браузере?")
            msg.setIcon(QMessageBox.Information)
            msg.setMinimumWidth(420)

            yes_button = msg.addButton("Да", QMessageBox.AcceptRole)
            msg.addButton("Закрыть", QMessageBox.RejectRole)

            msg.exec()

            if msg.clickedButton() is yes_button and info.url:
                import webbrowser
                webbrowser.open(info.url)
        else:
            QMessageBox.information(
                self,
                "Проверка обновлений",
                f"Установлена актуальная версия ({APP_VERSION}).",
            )
