# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from assets.styles import AURORA_LIGHT_PRO


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(AURORA_LIGHT_PRO)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
