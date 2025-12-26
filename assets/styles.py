# assets/styles.py

AURORA_LIGHT_PRO = """
/* ---------- БАЗА ---------- */
QMainWindow, QDialog, QWidget {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #F7FAFF,
        stop:1 #EEF6FF
    );
    color: #2F3B4D;
}

QLabel { color: #2F3B4D; }

/* крупные заголовки для BIG SCREEN */
QLabel#big_title {
    font-size: 42pt;
    font-weight: 800;
    color: #1D2A40;
}
QLabel#round_title {
    font-size: 32pt;
    font-weight: 800;
    color: #3A7AFE;
}
QLabel#timer_label {
    font-size: 56pt;
    font-weight: 700;
    color: #1D2A40;
}
QLabel#question_label {
    font-size: 40pt;
    font-weight: 800;
    color: #1D2A40;
}

/* ---------- КНОПКИ ---------- */
QPushButton {
    background-color: #E3ECFF;
    color: #1D2A40;
    border-radius: 8px;
    padding: 6px 14px;
    border: 1px solid #C4D6FF;
    font-weight: 600;
}

QLabel#lbl_update_badge {
    background-color: #EF4444;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #D6E3FF;
}

QPushButton:pressed {
    background-color: #C2D5FF;
}

/* первичная большая синяя кнопка */
QPushButton#btn_primary {
    background-color: #2F80FF;
    color: #FFFFFF;
    border: none;
}

QPushButton#btn_primary:hover {
    background-color: #3F8DFF;
}

QPushButton#btn_primary:pressed {
    background-color: #256BDB;
}


QPushButton#btn_add,
QPushButton#btn_remove {
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}

/* Добавить — яркий зелёный */
QPushButton#btn_add {
    background-color: #27AE60;
    color: #FFFFFF;
}
QPushButton#btn_add:hover {
    background-color: #2ECC71;
}

/* Удалить — яркий красный */
QPushButton#btn_remove {
    background-color: #E74C3C;
    color: #FFFFFF;
}
QPushButton#btn_remove:hover {
    background-color: #FF6B5A;
}

/* режим темы — более спокойная */
QPushButton#btn_theme {
    background-color: #F3F5FB;
    color: #2F3B4D;
    border: 1px solid #D0D7E6;
}

QPushButton#btn_theme:hover {
    background-color: #E7ECF7;
}

QPushButton#btn_close_big {
    background-color: #F8F0F0;
    color: #C0392B;
    border: 1px solid #F1D6D3;
}

QPushButton#btn_close_big:hover {
    background-color: #F4E2E2;
}

/* ---------- ТУМБЛЕРЫ ---------- */

/* контейнер текста */
QCheckBox {
    color: #2F3B4D;
    font-weight: 500;
    spacing: 10px;              /* расстояние между тумблером и текстом */
}

/* сам тумблер — «пилюля» */
QCheckBox::indicator {
    width: 38px;
    height: 20px;
    border-radius: 10px;
    background: #E2E8F5;
    border: 1px solid #C4D6FF;
    position: relative;
}

/* Qt не поддерживает ::before, поэтому имитируем кружок цветом:
   в выключенном состоянии — левый полукруг светлый */
QCheckBox::indicator:unchecked {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #FFFFFF,
        stop:0.5 #FFFFFF,
        stop:0.5 #E2E8F5,
        stop:1 #E2E8F5
    );
}

/* включено — «синий» тумблер */
QCheckBox::indicator:checked {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2F80FF,
        stop:0.5 #2F80FF,
        stop:0.5 #E2E8F5,
        stop:1 #E2E8F5
    );
    border-color: #2F80FF;
}

/* отключённый (будущая фича) */
QCheckBox:disabled {
    color: #B0B9C8;
}
QCheckBox::indicator:disabled {
    background: #E5E9F3;
    border-color: #D0D7E6;
}


/* ---------- ПОЛЯ ВВОДА ---------- */
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: white;
    border: 1px solid #E6EDF8;
    border-radius: 8px;
    padding: 6px;
    color: #2F3B4D;
    outline: none;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPlainTextEdit:focus {
    border: 2px solid #3A7AFE;
    outline: none;
}

/* ---------- ГРУППЫ / КАРТОЧКИ ---------- */
QGroupBox {
    border: 1px solid #D9E3F5;
    border-radius: 16px;
    margin-top: 12px;
    padding: 10px 12px 14px 12px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF,
        stop:1 #F4F7FF
    );
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #7A8BA8;
    font-size: 10pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* общая "карточка" (таблица команд в админке, big screen) */
QWidget[role="card"] {
    border-radius: 18px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #F8FBFF,
        stop:1 #EEF4FF
    );
    border: 1px solid #E0E8FA;
}

/* ---------- ТАБЛИЦЫ ---------- */
QTableWidget, QTableView {
    background: transparent;
    border: none;
    color: #2F3B4D;
    gridline-color: transparent;
    outline: none;
    selection-background-color: transparent;
}

QTableWidget:focus {
    outline: none;
    border: none;
}

/* big screen получает свои размеры шрифтов, админка задаёт font в коде */
QTableWidget::item {
    padding: 14px 10px;
    font-size: 14pt;
    font-weight: 600;
    color: #1D2A40;
    border: none;
    background-color: rgba(255, 255, 255, 0.0);
}

QTableWidget::item:alternate {
    background-color: rgba(58, 122, 254, 0.04);
}

QTableWidget::item:selected {
    background-color: rgba(58, 122, 254, 0.15);
    color: #1D2A40;
}

/* заголовки таблиц (в админке и на big screen, если нужны) */
QHeaderView::section {
    background: transparent;
    color: #1D2A40;
    font-size: 18pt;
    font-weight: 800;
    padding: 10px;
    border: none;
    outline: none;
}

QTableCornerButton::section {
    background: transparent;
    border: none;
}

/* ---------- МЕНЮ ---------- */
QMenu {
    background: white;
    border: 1px solid #E6EDF8;
    color: #2F3B4D;
}
QMenu::item:selected {
    background: #F0F5FF;
    color: #2F3B4D;
}

/* ---------- СКРОЛЛБАР ---------- */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #D0DFF6;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #B6CCF6;
}
"""


AURORA_DARK = """
/* ---------- БАЗА ---------- */
QMainWindow, QDialog, QWidget {
    background-color: #0E1117;
    color: #F4F6FB;
}

QLabel { color: #F4F6FB; }

/* заголовки для BIG SCREEN */
QLabel#big_title {
    font-size: 42pt;
    font-weight: 800;
    color: #F4F6FB;
}
QLabel#round_title {
    font-size: 32pt;
    font-weight: 800;
    color: #4EA4FF;
}
QLabel#timer_label {
    font-size: 56pt;
    font-weight: 700;
    color: #F4F6FB;
}
QLabel#question_label {
    font-size: 40pt;
    font-weight: 800;
    color: #F4F6FB;
}

/* ---------- КНОПКИ ---------- */

/* вторичные кнопки */
QPushButton {
    background-color: #111827;
    color: #F4F6FB;
    border-radius: 8px;
    padding: 6px 14px;
    border: 1px solid #374151;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1F2933;
}

QLabel#lbl_update_badge {
    background-color: #EF4444;
    border-radius: 5px; /* половина 10px */
}

/* первичная синяя (Показать большой экран) */
QPushButton#btn_primary {
    background-color: #2381E9;
    color: #FFFFFF;
    border: none;
}
QPushButton#btn_primary:hover {
    background-color: #1b65b6;
}

QPushButton#btn_add,
QPushButton#btn_remove {
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}

/* Добавить — приглушённый зелёный */
QPushButton#btn_add {
    background-color: #15803D;     /* темнее */
    color: #FFFFFF;
}
QPushButton#btn_add:hover {
    background-color: #16A34A;
}

/* Удалить — приглушённый красный */
QPushButton#btn_remove {
    background-color: #B91C1C;
    color: #FFFFFF;
}
QPushButton#btn_remove:hover {
    background-color: #DC2626;
}

/* кнопка "Закрыть" big screen чуть мягче */
QPushButton#btn_close_big {
    background-color: #111827;
    color: #FCA5A5;
    border: 1px solid #4B5563;
}
QPushButton#btn_close_big:hover {
    background-color: #1F2933;
}


/* ---------- ТУМБЛЕРЫ ---------- */

QCheckBox {
    color: #F4F6FB;
    font-weight: 500;
    spacing: 10px;
}

/* дорожка */
QCheckBox::indicator {
    width: 38px;
    height: 20px;
    border-radius: 10px;
    background: #020617;
    border: 1px solid #1F2937;
}

/* выключен */
QCheckBox::indicator:unchecked {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #020617,
        stop:1 #111827
    );
}

/* включен */
QCheckBox::indicator:checked {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2381E9,
        stop:0.5 #2381E9,
        stop:0.5 #020617,
        stop:1 #020617
    );
    border-color: #2381E9;
}

/* disabled */
QCheckBox:disabled {
    color: #6B7280;
}
QCheckBox::indicator:disabled {
    background: #020617;
    border-color: #374151;
}



/* ---------- ПОЛЯ ВВОДА ---------- */
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 6px;
    color: #F4F6FB;
    outline: none;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPlainTextEdit:focus {
    border: 2px solid #2381E9;
    outline: none;
}

/* ---------- ГРУППЫ / КАРТОЧКИ ---------- */
QGroupBox {
    border: 1px solid #30363D;
    border-radius: 16px;
    margin-top: 12px;
    padding: 10px 12px 14px 12px;
    background: #161B22;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #7A8BA8;
    font-size: 10pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* карточка с таблицей */
QWidget[role="card"] {
    border-radius: 18px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #111827,
        stop:1 #020617
    );
    border: 1px solid #1F2937;
}
QWidget[role="card"] QTableWidget {
    padding: 8px;
    outline: none;
}

/* ---------- ТАБЛИЦЫ ---------- */
QTableWidget, QTableView {
    background: transparent;
    border: none;
    color: #F4F6FB;
    gridline-color: transparent;
    outline: none;
    selection-background-color: transparent;
}
QTableWidget:focus {
    outline: none;
    border: none;
}

QTableWidget::item {
    padding: 14px 10px;
    font-size: 14pt;
    font-weight: 600;
    color: #F4F6FB;
    border: none;
    outline: none;
}

QTableWidget::item:alternate {
    background-color: rgba(15, 23, 42, 0.6);
}

/* лёгкий hover только для админки; big screen таблица без objectName остаётся статичной */
QTableWidget#adminTable::item:hover {
    background: rgba(60, 120, 255, 0.10);
}

QTableWidget::item:selected {
    background-color: rgba(35, 129, 233, 0.2);
    color: #F4F6FB;
}

QTableWidget::viewport,
QTableCornerButton::section {
    background-color: #0D1117;
}

/* заголовки таблиц */
QHeaderView::section {
    background: transparent;
    color: #F4F6FB;
    font-size: 18pt;
    font-weight: 800;
    padding: 10px;
    border: none;
    outline: none;
}

/* ---------- МЕНЮ ---------- */
QMenu {
    background: #161B22;
    border: 1px solid #30363D;
    color: #F4F6FB;
}
QMenu::item:selected {
    background: #2381E9;
    color: white;
}

/* ---------- СКРОЛЛБАР ---------- */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #30363D;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #4EA4FF;
}
"""
