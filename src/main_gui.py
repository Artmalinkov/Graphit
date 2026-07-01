# src/main_gui.py
"""
Точка входа для графического интерфейса Graphite
"""

import sys
from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main():
    """Запускает GUI приложения"""
    app = QApplication(sys.argv)

    # Устанавливаем стиль приложения
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()