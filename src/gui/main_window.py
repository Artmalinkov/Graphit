# src/gui/main_window.py
"""
Главное окно приложения Graphite
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame,
    QStackedWidget, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QAction

from src.work_db.session import get_session
from src.work_db.crud import get_all_persons, get_all_organizations, get_all_industries
from src.models import Gender


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphite")
        self.setMinimumSize(900, 650)

        # Инициализируем сессию БД
        self.session = get_session()

        # Настраиваем интерфейс
        self._setup_ui()
        self._setup_menu()

        # По умолчанию показываем список людей
        self.show_persons()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # ---- Заголовок ----
        header = QLabel("⚡ Graphite")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 24, QFont.Bold))
        main_layout.addWidget(header)

        # ---- Панель кнопок ----
        button_frame = QFrame()
        button_frame.setFrameShape(QFrame.StyledPanel)
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        # Кнопка "Люди"
        self.btn_persons = QPushButton("👤 Люди")
        self.btn_persons.setMinimumSize(150, 45)
        self.btn_persons.setStyleSheet(self._get_button_style())
        self.btn_persons.clicked.connect(self.show_persons)
        button_layout.addWidget(self.btn_persons)

        # Кнопка "Организации"
        self.btn_organizations = QPushButton("🏢 Организации")
        self.btn_organizations.setMinimumSize(150, 45)
        self.btn_organizations.setStyleSheet(self._get_button_style())
        self.btn_organizations.clicked.connect(self.show_organizations)
        button_layout.addWidget(self.btn_organizations)

        # Кнопка "Сферы деятельности"
        self.btn_industries = QPushButton("📊 Сферы деятельности")
        self.btn_industries.setMinimumSize(150, 45)
        self.btn_industries.setStyleSheet(self._get_button_style())
        self.btn_industries.clicked.connect(self.show_industries)
        button_layout.addWidget(self.btn_industries)

        main_layout.addWidget(button_frame)

        # ---- Стек для переключения контента ----
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Создаём страницы
        self.page_persons = self._create_persons_page()
        self.page_organizations = self._create_organizations_page()
        self.page_industries = self._create_industries_page()

        self.stacked_widget.addWidget(self.page_persons)
        self.stacked_widget.addWidget(self.page_organizations)
        self.stacked_widget.addWidget(self.page_industries)

    def _get_button_style(self):
        """Стиль для кнопок"""
        return """
            QPushButton {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:pressed {
                background-color: #45a049;
                border-color: #45a049;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                color: white;
            }
        """

    def _setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("&Файл")

        exit_action = QAction("В&ыход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню "Вид"
        view_menu = menubar.addMenu("&Вид")

        persons_action = QAction("&Люди", self)
        persons_action.setShortcut("Ctrl+1")
        persons_action.triggered.connect(self.show_persons)
        view_menu.addAction(persons_action)

        organizations_action = QAction("&Организации", self)
        organizations_action.setShortcut("Ctrl+2")
        organizations_action.triggered.connect(self.show_organizations)
        view_menu.addAction(organizations_action)

        industries_action = QAction("&Сферы деятельности", self)
        industries_action.setShortcut("Ctrl+3")
        industries_action.triggered.connect(self.show_industries)
        view_menu.addAction(industries_action)

    def _create_persons_page(self):
        """Создаёт страницу со списком людей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("👤 Список людей")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.list_persons = QListWidget()
        self.list_persons.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #e8f5e9;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
        layout.addWidget(self.list_persons)

        return widget

    def _create_organizations_page(self):
        """Создаёт страницу со списком организаций"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("🏢 Список организаций")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.list_organizations = QListWidget()
        self.list_organizations.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_organizations)

        return widget

    def _create_industries_page(self):
        """Создаёт страницу со списком сфер деятельности"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("📊 Список сфер деятельности")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.list_industries = QListWidget()
        self.list_industries.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_industries)

        return widget

    # ============================================================
    # Методы для отображения данных
    # ============================================================

    def show_persons(self):
        """Показывает список людей"""
        self.stacked_widget.setCurrentWidget(self.page_persons)
        self._load_persons()

    def show_organizations(self):
        """Показывает список организаций"""
        self.stacked_widget.setCurrentWidget(self.page_organizations)
        self._load_organizations()

    def show_industries(self):
        """Показывает список сфер деятельности"""
        self.stacked_widget.setCurrentWidget(self.page_industries)
        self._load_industries()

    def _load_persons(self):
        """Загружает людей из БД"""
        self.list_persons.clear()
        try:
            persons = get_all_persons(self.session)
            for person in persons:
                # Формируем отображаемое имя
                display_name = person.full_name or ''

                # Добавляем иконку пола (если указан)
                gender_icon = person.gender_icon if person.gender else ''
                if gender_icon:
                    display_name = f"{gender_icon} {display_name}"

                item = QListWidgetItem(display_name)

                # Добавляем дополнительную информацию
                info = []
                if person.birth_date:
                    info.append(f"р. {person.birth_date.strftime('%d.%m.%Y')}")
                if person.gender:
                    info.append(f"пол: {person.gender_display}")
                if person.notes:
                    info.append(f"📝 {person.notes[:30]}...")

                if info:
                    item.setText(f"{display_name} ({' | '.join(info)})")

                self.list_persons.addItem(item)

            if persons:
                self.list_persons.addItem(f"\n📊 Всего: {len(persons)} человек")
        except Exception as e:
            self.list_persons.addItem(f"❌ Ошибка загрузки: {e}")

    def _load_organizations(self):
        """Загружает организации из БД"""
        self.list_organizations.clear()
        try:
            organizations = get_all_organizations(self.session)
            for org in organizations:
                item = QListWidgetItem(f"🏢 {org.name}")
                if org.full_name:
                    item.setText(f"{org.name} ({org.full_name})")
                self.list_organizations.addItem(item)

            if organizations:
                self.list_organizations.addItem(f"\n📊 Всего: {len(organizations)} организаций")
        except Exception as e:
            self.list_organizations.addItem(f"❌ Ошибка загрузки: {e}")

    def _load_industries(self):
        """Загружает сферы деятельности из БД"""
        self.list_industries.clear()
        try:
            industries = get_all_industries(self.session)
            for industry in industries:
                item = QListWidgetItem(f"📊 {industry.name}")
                if industry.description:
                    item.setText(f"{industry.name} — {industry.description}")
                self.list_industries.addItem(item)

            if industries:
                self.list_industries.addItem(f"\n📊 Всего: {len(industries)} сфер")
        except Exception as e:
            self.list_industries.addItem(f"❌ Ошибка загрузки: {e}")

    def closeEvent(self, event):
        """Закрывает сессию БД при закрытии окна"""
        self.session.close()
        event.accept()