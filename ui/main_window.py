# ui/main_window.py
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QGroupBox, QPlainTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QMenu
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

from core.update_checker import fetch_latest_release
from core.version import APP_VERSION


APP_STATE = 'quiz_state.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quiz Admin — Aurora Light')
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

        # left column - teams and history
        left_col = QVBoxLayout()
        teams_box = QGroupBox('Команды')
        tb_layout = QVBoxLayout(teams_box)
        top_row = QHBoxLayout()
        self.btn_add = QPushButton('Добавить команду')
        self.btn_remove = QPushButton('Удалить')
        top_row.addWidget(self.btn_add); top_row.addWidget(self.btn_remove); top_row.addStretch()
        tb_layout.addLayout(top_row)

        # card container for table
        self.table_card = QWidget()
        self.table_card.setProperty('role', 'card')
        card_layout = QVBoxLayout(self.table_card)
        card_layout.setContentsMargins(6, 6, 6, 6)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(['Команда', 'Очки'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        card_layout.addWidget(self.table)
        tb_layout.addWidget(self.table_card)
        left_col.addWidget(teams_box, 3)

        hist_box = QGroupBox('История')
        hb_layout = QVBoxLayout()
        self.hist = QPlainTextEdit(); self.hist.setReadOnly(True)
        hb_layout.addWidget(self.hist); hist_box.setLayout(hb_layout)
        left_col.addWidget(hist_box, 1)

        body.addLayout(left_col, 3)

        # right column - controls
        right_col = QVBoxLayout()
        round_box = QGroupBox('Раунд')
        rb_layout = QVBoxLayout()
        rname_layout = QHBoxLayout()
        self.round_name = QLineEdit('Раунд 1')
        rname_layout.addWidget(QLabel('Вопрос:')); rname_layout.addWidget(self.round_name)
        rb_layout.addLayout(rname_layout)

        time_layout = QHBoxLayout()
        self.spin_minutes = QSpinBox(); self.spin_minutes.setRange(0, 999); self.spin_minutes.setValue(1)
        self.spin_seconds = QSpinBox(); self.spin_seconds.setRange(0, 59); self.spin_seconds.setValue(0)
        time_layout.addWidget(QLabel('Мин:')); time_layout.addWidget(self.spin_minutes)
        time_layout.addWidget(QLabel('Сек:')); time_layout.addWidget(self.spin_seconds)
        rb_layout.addLayout(time_layout)

        btns = QHBoxLayout()
        self.btn_start = QPushButton('Старт'); self.btn_pause = QPushButton('Пауза'); self.btn_reset = QPushButton('Сброс')
        btns.addWidget(self.btn_start); btns.addWidget(self.btn_pause); btns.addWidget(self.btn_reset)
        rb_layout.addLayout(btns)

        # pick image & show big screen
        img_row = QHBoxLayout()
        self.btn_pick_image = QPushButton('Выбрать картинку')
        self.btn_show_big = QPushButton('Показать большой экран')
        img_row.addWidget(self.btn_pick_image); img_row.addWidget(self.btn_show_big)
        rb_layout.addLayout(img_row)

        round_box.setLayout(rb_layout)
        right_col.addWidget(round_box)

        io_box = QHBoxLayout()
        self.btn_save = QPushButton('Сохранить')
        self.btn_load = QPushButton('Загрузить')
        self.btn_check_update = QPushButton(f'Проверить обновление (v{APP_VERSION})')
        io_box.addWidget(self.btn_save)
        io_box.addWidget(self.btn_load)
        io_box.addWidget(self.btn_check_update)
        right_col.addLayout(io_box)
        right_col.addStretch()
        body.addLayout(right_col, 2)

        # big screen instance
        self.big = BigScreenWindow()

        # current image path
        self.current_image = None

        # запомненный монитор
        self.big_screen_index = None

        # connections
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

        # синхронизация заголовка раунда с big screen
        self.round_name.textChanged.connect(self.big.set_round_title)

        # ui sync
        self.ui_timer = QTimer(self)
        self.ui_timer.setInterval(400)
        self.ui_timer.timeout.connect(self.refresh)
        self.ui_timer.start()

        # try load existing
        if os.path.exists(APP_STATE):
            try: self.load_state(APP_STATE)
            except Exception: pass

    def add_team(self):
        name = ask_team_name(self)
        if not name: return
        self.tm.add_team(name); self.lg.log(f'Добавлена команда: {name}'); self.refresh()

    def remove_selected(self):
        rows = sorted({i.row() for i in self.table.selectedIndexes()}, reverse=True)
        if not rows:
            QMessageBox.information(self, 'Удаление', 'Выберите хотя бы одну команду.')
            return
        for r in rows:
            self.tm.remove_by_index(r)
        self.lg.log('Удалены команды')
        self.refresh()

    def open_menu(self, pos):
        row = self.table.indexAt(pos).row()
        if row < 0: return
        m = QMenu(self)
        for txt, val in [('+1',1),('+5',5),('-1',-1),('-5',-5)]:
            act = QAction(txt, self); act.triggered.connect(lambda _, v=val: self.tm.adjust(row, v)); m.addAction(act)
        m.exec(self.table.viewport().mapToGlobal(pos)); self.refresh()

    def set_question_text(self, text: str):
        self.big.set_question(text)

    def refresh(self):
        teams = self.tm.teams
        self.table.setRowCount(len(teams))
        for i, t in enumerate(teams):
            self.table.setItem(i, 0, QTableWidgetItem(t['name']))
            sc = QTableWidgetItem(str(t['score']))
            sc.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, sc)
            self.table.setRowHeight(i, 54)
        self.hist.setPlainText(self.lg.get_text())
        self.big.update_scores(self.tm.get_sorted())
        if self.current_image:
            self.big.set_round_image(self.current_image)
        self.big.set_round_title(self.round_name.text())


    def pick_image(self):
        p, _ = QFileDialog.getOpenFileName(self, 'Выберите изображение', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if not p: return
        self.current_image = p; self.lg.log(f'Выбрано изображение: {os.path.basename(p)}'); self.big.set_round_image(p)

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


    def start_timer(self):
        sec = self.spin_minutes.value()*60 + self.spin_seconds.value()
        if sec <= 0: QMessageBox.warning(self, 'Таймер', 'Установите длительность > 0.'); return
        self.timer.start(sec, callback=self._on_tick, finished=self._on_finish); self.lg.log('Таймер старт')

    def pause_timer(self):
        self.timer.toggle_pause(); self.lg.log('Пауза/Продолжение')

    def reset_timer(self):
        self.timer.reset(); self.lg.log('Таймер сброшен'); self._on_tick()

    def _on_tick(self):
        txt = self._timer_text() if self.timer.running else '--:--'
        self.big.update_timer(txt)

    def _on_finish(self):
        self.lg.log('Таймер завершён')
        self._on_tick()

    def _timer_text(self):
        return self.timer.format_time(self.timer.remaining)

    def save_state(self):
        state = self.sm.build_state(self.tm, self.lg, self.th, self.timer, self.round_name.text())
        try: self.sm.save(APP_STATE, state); self.lg.log('Состояние сохранено')
        except Exception as e: QMessageBox.critical(self, 'Ошибка', str(e))

    def check_update(self):
        from core.update_checker import fetch_latest_release
        from core.version import APP_VERSION

        try:
            info = fetch_latest_release()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Проверка обновлений",
                f"Не удалось проверить обновление:\n{e}"
            )
            return

        if info.has_update:
            msg = QMessageBox(self)
            msg.setWindowTitle("Доступно обновление")
            msg.setText(f"Текущая версия: {info.current}\nНовая версия: {info.latest}")
            msg.setInformativeText("Открыть страницу релиза в браузере?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setIcon(QMessageBox.Information)
            if msg.exec() == QMessageBox.Yes and info.url:
                import webbrowser
                webbrowser.open(info.url)
        else:
            QMessageBox.information(
                self,
                "Проверка обновлений",
                f"Установлена актуальная версия ({APP_VERSION})."
            )


    def load_state(self, path):
        data = self.sm.load(path)
        self.tm.load_from(data.get('teams', []))
        self.lg.load_from(data.get('history', []))

        rn = data.get('round_name')
        if rn:
            self.round_name.setText(rn)

        remaining = data.get('remaining')
        if isinstance(remaining, int) and remaining >= 0:
            self.timer.remaining = remaining
            mins, secs = divmod(remaining, 60)
            self.spin_minutes.setValue(mins)
            self.spin_seconds.setValue(secs)

        theme = data.get('theme')
        if theme:
            self.th.apply(theme)
            # сюда можно добавить применение темы к окнам

        self.refresh()

    
    def load_state_dialog(self):
        p, _ = QFileDialog.getOpenFileName(self, 'Загрузить состояние', '', 'JSON files (*.json)')
        if p: self.load_state(p)
