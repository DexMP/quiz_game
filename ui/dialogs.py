# ui/dialogs.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QInputDialog, QFileDialog, QApplication
from PySide6.QtCore import Qt

class MonitorChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите монитор")
        l = QVBoxLayout(self)
        self.list = QListWidget()
        l.addWidget(self.list)

        # Заполняем список доступных экранов
        for i, screen in enumerate(QApplication.screens()):
            g = screen.geometry()
            it = QListWidgetItem(f"Монитор {i+1}: {g.width()}x{g.height()} ({g.x()},{g.y()})")
            it.setData(Qt.UserRole, i)
            self.list.addItem(it)

        row = QHBoxLayout()
        ok = QPushButton("Выбрать"); cancel = QPushButton("Отмена")
        ok.clicked.connect(self.accept); cancel.clicked.connect(self.reject)
        row.addStretch(); row.addWidget(cancel); row.addWidget(ok)
        l.addLayout(row)

    def selected_index(self):
        it = self.list.currentItem()
        return None if not it else it.data(Qt.UserRole)

def ask_team_name(parent):
    text, ok = QInputDialog.getText(parent, "Новая команда", "Имя команды:")
    return text.strip() if ok and text.strip() else None

def ask_file_open(parent, caption="Выберите файл", flt="*"):
    p, _ = QFileDialog.getOpenFileName(parent, caption, "", flt)
    return p or None
