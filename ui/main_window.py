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
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

from ui.big_screen import BigScreenWindow
from ui.dialogs import MonitorChoiceDialog, ask_team_name
from core.team_manager import TeamManager
from core.timer_controller import TimerController
from core.theme_manager import ThemeManager
from core.state_manager import StateManager
from core.logger import Logger
from assets.styles import AURORA_LIGHT_PRO, AURORA_DARK
from core.update_checker import fetch_latest_release
from core.version import APP_VERSION

APP_STATE = "quiz_state.json"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Admin — Aurora Light")
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
        top_row.addWidget(self.btn_add)
        top_row.addWidget(self.btn_remove)
        top_row.addStretch()
        tb_layout.addLayout(top_row)

        # таблица команд
        self.table_card = QWidget()
        self.table_card.setProperty("role", "card")
        card_layout = QVBoxLayout(self.table_card)
        card_layout.setContentsMargins(6, 6, 6, 6)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Команда", "Очки"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
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

        # правая колонка — переработанное меню
        right_col = QVBoxLayout()
        
        # Вопрос
        question_box = QGroupBox("Вопрос")
        q_layout = QVBoxLayout()
        self.question_text = QLineEdit("")
        self.question_text.setPlaceholderText("Введите текст вопроса...")
        q_layout.addWidget(self.question_text)
        question_box.setLayout(q_layout)
        right_col.addWidget(question_box)

        # Таймер
        timer_box = QGroupBox("Таймер")
        timer_layout = QVBoxLayout()
        
        # Длительность
        time_row = QHBoxLayout()
        time_row.addWidget(QLabel("Мин:"))
        self.spin_minutes = QSpinBox()
        self.spin_minutes.setRange(0, 999)
        self.spin_minutes.setValue(1)
        self.spin_minutes.setMinimumWidth(80)
        time_row.addWidget(self.spin_minutes)
        time_row.addWidget(QLabel("Сек:"))
        self.spin_seconds = QSpinBox()
        self.spin_seconds.setRange(0, 59)
        self.spin_seconds.setValue(0)
        self.spin_seconds.setMinimumWidth(80)
        time_row.addWidget(self.spin_seconds)
        time_row.addStretch()
        timer_layout.addLayout(time_row)
        
        # Кнопки таймера
        btns = QHBoxLayout()
        self.btn_start = QPushButton("Старт")
        self.btn_pause = QPushButton("Пауза")
        self.btn_reset = QPushButton("Сброс")
        self.btn_start.setMinimumHeight(40)
        self.btn_pause.setMinimumHeight(40)
        self.btn_reset.setMinimumHeight(40)
        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_pause)
        btns.addWidget(self.btn_reset)
        timer_layout.addLayout(btns)
        
        timer_box.setLayout(timer_layout)
        right_col.addWidget(timer_box)

        # Большой экран
        screen_box = QGroupBox("Большой экран")
        screen_layout = QVBoxLayout()
        
        self.btn_pick_image = QPushButton("Выбрать картинку")
        self.btn_pick_image.setMinimumHeight(40)
        screen_layout.addWidget(self.btn_pick_image)
        
        self.btn_show_big = QPushButton("Показать большой экран")
        self.btn_show_big.setMinimumHeight(40)
        screen_layout.addWidget(self.btn_show_big)
        
        screen_box.setLayout(screen_layout)
        right_col.addWidget(screen_box)

        # Настройки
        settings_box = QGroupBox("Настройки")
        settings_layout = QVBoxLayout()
        
        io_row1 = QHBoxLayout()
        self.btn_save = QPushButton("Сохранить")
        self.btn_load = QPushButton("Загрузить")
        self.btn_save.setMinimumHeight(40)
        self.btn_load.setMinimumHeight(40)
        io_row1.addWidget(self.btn_save)
        io_row1.addWidget(self.btn_load)
        settings_layout.addLayout(io_row1)
        
        self.btn_theme = QPushButton("Тёмная тема")
        self.btn_theme.setMinimumHeight(40)
        settings_layout.addWidget(self.btn_theme)
        
        self.btn_check_update = QPushButton(f"Проверить обновление (v{APP_VERSION})")
        self.btn_check_update.setMinimumHeight(40)
        settings_layout.addWidget(self.btn_check_update)
        
        settings_box.setLayout(settings_layout)
        right_col.addWidget(settings_box)
        
        right_col.addStretch()
        body.addLayout(right_col, 2)

        # big screen
        self.big = BigScreenWindow()

        # состояние
        self.current_image = None
        self.big_screen_index = None

        # сигналы
        self.btn_add.clicked.connect(self.add_team)
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_start.clicked.connect(self.start_timer)
        self.btn_pause.clicked.connect(self.pause_timer)
        self.btn_reset.clicked.connect(self.reset_timer)
        self.btn_pick_image.clicked.connect(self.pick_image)
        self.btn_show_big.clicked.connect(self.show_big)
        self.btn_save.clicked.connect(self.save_state)
        self.btn_load.clicked.connect(self.load_state_dialog)
        self.btn_check_update.clicked.connect(self.check_update)
        self.btn_theme.clicked.connect(self.toggle_theme)

        self.question_text.textChanged.connect(self.set_question_text)

        # периодический рефреш
        self.ui_timer = QTimer(self)
        self.ui_timer.setInterval(400)
        self.ui_timer.timeout.connect(self.refresh)
        self.ui_timer.start()

        # пробуем загрузить состояние
        if os.path.exists(APP_STATE):
            try:
                self.load_state(APP_STATE)
            except Exception:
                pass

    # -------- команды и таблица --------

    def add_team(self):
        name = ask_team_name(self)
        if not name:
            return
        self.tm.add_team(name)
        self.lg.log(f"Добавлена команда: {name}")
        self.refresh()

    def remove_selected(self):
        rows = sorted(
            {i.row() for i in self.table.selectedIndexes()}, reverse=True
        )
        if not rows:
            QMessageBox.information(
                self, "Удаление", "Выберите хотя бы одну команду."
            )
            return
        for r in rows:
            self.tm.remove_by_index(r)
        self.lg.log("Удалены команды")
        self.refresh()

    def open_menu(self, pos):
        row = self.table.indexAt(pos).row()
        if row < 0:
            return
        m = QMenu(self)
        for txt, val in [("+1", 1), ("+5", 5), ("-1", -1), ("-5", -5)]:
            act = QAction(txt, self)
            act.triggered.connect(
                lambda _, v=val: self.tm.adjust(row, v)
            )
            m.addAction(act)
        m.exec(self.table.viewport().mapToGlobal(pos))
        self.refresh()

    def set_question_text(self, text: str):
        self.big.set_question(text)

    def refresh(self):
        teams = self.tm.teams
        self.table.setRowCount(len(teams))
        for i, t in enumerate(teams):
            self.table.setItem(i, 0, QTableWidgetItem(t["name"]))
            sc = QTableWidgetItem(str(t["score"]))
            sc.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, sc)
            self.table.setRowHeight(i, 54)
        self.hist.setPlainText(self.lg.get_text())
        self.big.update_scores(self.tm.get_sorted())
        if self.current_image:
            self.big.set_round_image(self.current_image)

    # -------- big screen / изображение --------

    def pick_image(self):
        p, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)",
        )
        if not p:
            return
        self.current_image = p
        self.lg.log(f"Выбрано изображение: {os.path.basename(p)}")
        self.big.set_round_image(p)

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

    # -------- таймер --------

    def start_timer(self):
        sec = self.spin_minutes.value() * 60 + self.spin_seconds.value()
        if sec <= 0:
            QMessageBox.warning(
                self, "Таймер", "Установите длительность > 0."
            )
            return
        self.timer.start(sec, callback=self._on_tick, finished=self._on_finish)
        self.lg.log("Таймер старт")

    def pause_timer(self):
        self.timer.toggle_pause()
        if self.timer.running:
            self.btn_pause.setText("Пауза")
            self.lg.log("Таймер продолжен")
        else:
            self.btn_pause.setText("Продолжить")
            self.lg.log("Таймер на паузе")

    def reset_timer(self):
        self.timer.reset()
        self.lg.log("Таймер сброшен")
        self.btn_pause.setText("Пауза")
        self._on_tick()

    def _on_tick(self):
        txt = self._timer_text() if self.timer.running else "--:--"
        self.big.update_timer(txt)

    def _on_finish(self):
        self.lg.log("Таймер завершён")
        self._on_tick()

    def _timer_text(self):
        return self.timer.format_time(self.timer.remaining)

    # -------- состояние --------

    def save_state(self):
        state = self.sm.build_state(
            self.tm,
            self.lg,
            self.th,
            self.timer,
            "",  # больше не сохраняем название раунда
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
            mins, secs = divmod(remaining, 60)
            self.spin_minutes.setValue(mins)
            self.spin_seconds.setValue(secs)

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
            self.btn_theme.setText("Светлая тема")
        else:
            app.setStyleSheet(AURORA_LIGHT_PRO)
            self.btn_theme.setText("Тёмная тема")

    def toggle_theme(self):
        self.th.toggle_mode()
        self.apply_theme_from_state()

    # -------- обновление --------

    def check_update(self):
        try:
            info = fetch_latest_release()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Проверка обновлений",
                f"Не удалось проверить обновление:\n{e}",
            )
            return

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
