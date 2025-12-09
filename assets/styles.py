# assets/styles.py
AURORA_LIGHT_PRO = """
QMainWindow, QDialog, QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F7FAFF, stop:1 #EEF6FF);
    color: #2F3B4D;
}

QLabel { color: #2F3B4D; }
QLabel#big_title { font-size: 42pt; font-weight: 800; color: #1D2A40; }
QLabel#round_title { font-size: 28pt; font-weight: 700; color: #1D2A40; }
QLabel#timer_label { font-size: 84pt; font-weight: 900; color: #3A7AFE; }

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
QTableWidget::item { padding: 10px 6px; }
QHeaderView::section {
    background: transparent;
    color: #2F3B4D;
    font-weight: 700;
    padding: 8px;
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

QLabel#question_label {
    font-size: 40pt;
    font-weight: 800;
    color: #1D2A40;
}

QTableWidget::item {
    padding: 14px 10px;
    font-size: 24pt;
    font-weight: 700;
}
QHeaderView::section {
    font-size: 20pt;
}

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
