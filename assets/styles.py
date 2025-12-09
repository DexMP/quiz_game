# assets/styles.py
AURORA_LIGHT_PRO = """
QMainWindow, QDialog, QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F7FAFF, stop:1 #EEF6FF);
    color: #2F3B4D;
}

QLabel { color: #2F3B4D; }
QLabel#big_title { font-size: 42pt; font-weight: 800; color: #1D2A40; }

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

QPushButton {
    background-color: #3A7AFE;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
QPushButton:hover { background-color: #2f66e6; }
QPushButton#ghost {
    background: transparent;
    color: #2F3B4D;
    border: 1px solid rgba(47,59,77,0.08);
}

QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: white;
    border: 1px solid #E6EDF8;
    border-radius: 8px;
    padding: 6px;
    color: #2F3B4D;
}
QGroupBox {
    background: white;
    border: 1px solid #E6EDF8;
    border-radius: 12px;
    padding: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #51607A;
}

QTableWidget, QTableView {
    background: transparent;
    border: none;
    color: #2F3B4D;
}

/* строки таблицы команд */
QTableWidget::item {
    padding: 20px 18px;
    font-size: 32pt;
    font-weight: 800;
    color: #1D2A40;
    border-bottom: 2px solid rgba(29, 42, 64, 0.15);
}
/* у последней строки без разделителя */
QTableWidget::item:last-child {
    border-bottom: none;
}

QHeaderView::section {
    background: transparent;
    color: #1D2A40;
    font-size: 24pt;
    font-weight: 800;
    padding: 10px;
    border: none;
}
QTableCornerButton::section {
    background: transparent;
    border: none;
}

QWidget[role="card"] {
    background: white;
    border-radius: 12px;
    border: 1px solid #E6EDF8;
}
QWidget[role="card"] QTableWidget { padding: 8px; }

QMenu {
    background: white;
    border: 1px solid #E6EDF8;
    color: #2F3B4D;
}
QMenu::item:selected { background: #F0F5FF; }

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #D0DFF6;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #B6CCF6; }
"""

AURORA_DARK = """
QMainWindow, QDialog, QWidget {
    background-color: #0E1117;
    color: #F4F6FB;
}

QLabel { color: #F4F6FB; }
QLabel#big_title { font-size: 42pt; font-weight: 800; color: #F4F6FB; }

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

QPushButton {
    background-color: #2381E9;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
QPushButton:hover { background-color: #1b65b6; }

QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 6px;
    color: #F4F6FB;
}
QGroupBox {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #8B949E;
}

QTableWidget, QTableView {
    background: transparent;
    border: none;
    color: #F4F6FB;
}

QTableWidget::item {
    padding: 20px 18px;
    font-size: 32pt;
    font-weight: 800;
    color: #F4F6FB;
    border-bottom: 2px solid rgba(240, 246, 252, 0.15);
}
QTableWidget::item:last-child {
    border-bottom: none;
}

QHeaderView::section {
    background: transparent;
    color: #F4F6FB;
    font-size: 24pt;
    font-weight: 800;
    padding: 10px;
    border: none;
}

QWidget[role="card"] {
    background: #0D1117;
    border-radius: 12px;
    border: 1px solid #30363D;
}
QWidget[role="card"] QTableWidget { padding: 8px; }

QMenu {
    background: #161B22;
    border: 1px solid #30363D;
    color: #F4F6FB;
}
QMenu::item:selected { background: #2381E9; }

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #30363D;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #4EA4FF; }
"""
