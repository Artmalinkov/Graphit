# src/gui/main_window.py
"""
Главное окно приложения Graphite
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon

from src.work_db.session import get_session
from src.gui.graph_window import GraphWindow
from src.gui.persons_window import PersonsWindow
from src.gui.organizations_window import OrganizationsWindow
from src.gui.industries_window import IndustriesWindow


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphite")
        self.setMinimumSize(750, 550)
        self.setMaximumSize(900, 650)

        # Инициализируем сессию БД
        self.session = get_session()

        # Настраиваем интерфейс
        self._setup_ui()

        # Словарь для хранения открытых окон
        self.open_windows = {}

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ---- Заголовок ----
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(5)

        # Логотип
        logo_label = QLabel("⚡")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 48))
        header_layout.addWidget(logo_label)

        # Название
        title = QLabel("Graphite")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 28, QFont.Bold))
        header_layout.addWidget(title)

        # Подзаголовок
        subtitle = QLabel("Визуализация социальных связей")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #666;")
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # ---- Разделитель ----
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)

        # ---- Панель с кнопками (4 карточки в сетке 2x2) ----
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        cards_layout.setAlignment(Qt.AlignCenter)

        # Кнопка "Граф"
        self.btn_graph = self._create_card_button(
            "🕸️", "Граф",
            "Визуализация связей",
            self.open_graph_window
        )
        cards_layout.addWidget(self.btn_graph, 0, 0)

        # Кнопка "Люди"
        self.btn_persons = self._create_card_button(
            "👤", "Люди",
            "Управление людьми",
            self.open_persons_window
        )
        cards_layout.addWidget(self.btn_persons, 0, 1)

        # Кнопка "Организации"
        self.btn_organizations = self._create_card_button(
            "🏢", "Организации",
            "Управление организациями",
            self.open_organizations_window
        )
        cards_layout.addWidget(self.btn_organizations, 1, 0)

        # Кнопка "Сферы деятельности"
        self.btn_industries = self._create_card_button(
            "📊", "Сферы деятельности",
            "Управление сферами",
            self.open_industries_window
        )
        cards_layout.addWidget(self.btn_industries, 1, 1)

        main_layout.addLayout(cards_layout)

        # ---- Строка статуса ----
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("✅ База данных готова")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
        status_layout.addWidget(self.status_label)

        main_layout.addLayout(status_layout)

    def _create_card_button(self, icon: str, title: str, description: str, callback):
        """Создаёт карточку-кнопку"""
        button = QPushButton()
        button.setFixedSize(180, 200)
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #4CAF50;
            }
            QPushButton:pressed {
                background-color: #e8f5e9;
                border-color: #388E3C;
            }
        """)
        button.clicked.connect(callback)

        # Layout кнопки
        layout = QVBoxLayout(button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        # Иконка
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 48))
        layout.addWidget(icon_label)

        # Название
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)

        # Описание
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet("color: #888;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Кнопка "Открыть"
        open_btn = QPushButton("Открыть →")
        open_btn.setFixedSize(100, 30)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        open_btn.clicked.connect(callback)
        layout.addWidget(open_btn)

        return button

    # ============================================================
    # Методы для открытия окон
    # ============================================================

    def open_graph_window(self):
        """Открывает окно с графом"""
        if "graph" not in self.open_windows or not self.open_windows["graph"].isVisible():
            window = GraphWindow(self.session)
            window.setWindowModality(Qt.WindowModality.ApplicationModal)
            window.show()
            self.open_windows["graph"] = window
        else:
            self.open_windows["graph"].raise_()
            self.open_windows["graph"].activateWindow()

    def open_persons_window(self):
        """Открывает окно со списком людей"""
        if "persons" not in self.open_windows or not self.open_windows["persons"].isVisible():
            window = PersonsWindow(self.session)
            window.setWindowModality(Qt.WindowModality.ApplicationModal)
            window.show()
            self.open_windows["persons"] = window
        else:
            self.open_windows["persons"].raise_()
            self.open_windows["persons"].activateWindow()

    def open_organizations_window(self):
        """Открывает окно со списком организаций"""
        if "organizations" not in self.open_windows or not self.open_windows["organizations"].isVisible():
            window = OrganizationsWindow(self.session)
            window.setWindowModality(Qt.WindowModality.ApplicationModal)
            window.show()
            self.open_windows["organizations"] = window
        else:
            self.open_windows["organizations"].raise_()
            self.open_windows["organizations"].activateWindow()

    def open_industries_window(self):
        """Открывает окно со списком сфер деятельности"""
        if "industries" not in self.open_windows or not self.open_windows["industries"].isVisible():
            window = IndustriesWindow(self.session)
            window.setWindowModality(Qt.WindowModality.ApplicationModal)
            window.show()
            self.open_windows["industries"] = window
        else:
            self.open_windows["industries"].raise_()
            self.open_windows["industries"].activateWindow()

    def closeEvent(self, event):
        """Закрывает все дочерние окна и сессию БД"""
        for window in self.open_windows.values():
            if window.isVisible():
                window.close()
        self.session.close()
        event.accept()