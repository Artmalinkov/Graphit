# src/gui/main_window.py
"""
Главное окно приложения Graphite — дашборд
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame,
    QStackedWidget, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.work_db.session import get_session
from src.work_db.crud import get_all_persons, get_all_organizations, get_all_industries
from src.models import Gender


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphite")
        self.setMinimumSize(420, 700)
        self.setMaximumWidth(520)

        # Инициализируем сессию БД
        self.session = get_session()

        # Настраиваем интерфейс
        self._setup_ui()
        self._setup_menu()

        # По умолчанию показываем дашборд
        self.show_dashboard()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # ---- Заголовок ----
        header = QLabel("⚡ Graphite")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 28, QFont.Bold))
        main_layout.addWidget(header)

        subtitle = QLabel("Визуализация социальных связей")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #888;")
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        # ---- Стек для переключения контента ----
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Создаём страницы
        self.page_dashboard = self._create_dashboard_page()
        self.page_persons = self._create_persons_page()
        self.page_organizations = self._create_organizations_page()
        self.page_industries = self._create_industries_page()

        self.stacked_widget.addWidget(self.page_dashboard)
        self.stacked_widget.addWidget(self.page_persons)
        self.stacked_widget.addWidget(self.page_organizations)
        self.stacked_widget.addWidget(self.page_industries)

    def _create_primary_card(self, icon: str, title: str, description: str, callback):
        """
        Создаёт большую карточку (Граф) — на всю ширину
        """
        card = QPushButton()
        card.setMinimumHeight(110)
        card.setMaximumWidth(470)
        card.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 14px;
                padding: 22px 28px;
                text-align: center;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border-color: #4CAF50;
            }
            QPushButton:pressed {
                background-color: #f0f0f0;
            }
        """)
        card.clicked.connect(callback)

        # Внутренний layout для карточки
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)

        # Иконка и заголовок
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 22))
        title_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_layout.addWidget(title_label)

        layout.addLayout(title_layout)

        # Описание
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 13))
        desc_label.setStyleSheet("color: #888;")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        # Анимация при наведении
        def on_enter(event):
            card.setMinimumHeight(card.minimumHeight() + 5)

        def on_leave(event):
            card.setMinimumHeight(card.minimumHeight() - 5)

        card.enterEvent = on_enter
        card.leaveEvent = on_leave

        return card

    def _create_small_card(self, icon: str, title: str, callback):
        """
        Создаёт маленькую карточку (Люди, Организации, Сферы) — центрированную
        """
        card = QPushButton()
        card.setMinimumHeight(65)
        card.setMaximumWidth(380)  # Увеличено с 280 до 380
        card.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 12px;
                padding: 12px 20px;
                text-align: center;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border-color: #4CAF50;
            }
            QPushButton:pressed {
                background-color: #f0f0f0;
            }
        """)
        card.clicked.connect(callback)

        layout = QHBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 18))
        layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)

        def on_enter(event):
            card.setMinimumHeight(card.minimumHeight() + 5)
            card.setMaximumWidth(card.maximumWidth() + 10)

        def on_leave(event):
            card.setMinimumHeight(card.minimumHeight() - 5)
            card.setMaximumWidth(card.maximumWidth() - 10)

        card.enterEvent = on_enter
        card.leaveEvent = on_leave

        return card

        # Анимация при наведении
        def on_enter(event):
            card.setMinimumHeight(card.minimumHeight() + 5)
            card.setMaximumWidth(card.maximumWidth() + 10)

        def on_leave(event):
            card.setMinimumHeight(card.minimumHeight() - 5)
            card.setMaximumWidth(card.maximumWidth() - 10)

        card.enterEvent = on_enter
        card.leaveEvent = on_leave

        return card

    def _create_dashboard_page(self):
        """Создаёт страницу дашборда"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignTop)

        # ---- Большая карточка "Граф" (на всю ширину) ----
        card_graph = self._create_primary_card(
            "🕸️", "Граф", "Визуализация связей", self.show_graph
        )
        layout.addWidget(card_graph, alignment=Qt.AlignCenter)

        layout.addSpacing(8)

        # ---- Маленькие карточки (центрированные) ----
        card_persons = self._create_small_card(
            "👤", "Люди", self.show_persons
        )
        layout.addWidget(card_persons, alignment=Qt.AlignCenter)

        card_orgs = self._create_small_card(
            "🏢", "Организации", self.show_organizations
        )
        layout.addWidget(card_orgs, alignment=Qt.AlignCenter)

        card_industries = self._create_small_card(
            "📊", "Сферы", self.show_industries
        )
        layout.addWidget(card_industries, alignment=Qt.AlignCenter)

        layout.addSpacing(8)

        # ---- Статус базы данных ----
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f5e9;
                border-radius: 8px;
                padding: 8px 16px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setAlignment(Qt.AlignCenter)

        status_label = QLabel("✅ База данных готова")
        status_label.setFont(QFont("Arial", 11))
        status_label.setStyleSheet("color: #2e7d32;")
        status_layout.addWidget(status_label)

        layout.addWidget(status_frame, alignment=Qt.AlignCenter)

        # Растягивающийся элемент
        layout.addStretch()

        return widget

    def _create_persons_page(self):
        """Создаёт страницу со списком людей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Заголовок с кнопкой "Назад"
        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Назад")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("👤 Список людей")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        self.list_persons = QListWidget()
        self.list_persons.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
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

        self.persons_count_label = QLabel("")
        self.persons_count_label.setAlignment(Qt.AlignCenter)
        self.persons_count_label.setStyleSheet("color: #888; margin-top: 5px;")
        layout.addWidget(self.persons_count_label)

        return widget

    def _create_organizations_page(self):
        """Создаёт страницу со списком организаций"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Назад")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("🏢 Список организаций")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        self.list_organizations = QListWidget()
        self.list_organizations.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_organizations)

        self.orgs_count_label = QLabel("")
        self.orgs_count_label.setAlignment(Qt.AlignCenter)
        self.orgs_count_label.setStyleSheet("color: #888; margin-top: 5px;")
        layout.addWidget(self.orgs_count_label)

        return widget

    def _create_industries_page(self):
        """Создаёт страницу со списком сфер деятельности"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Назад")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("📊 Список сфер деятельности")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        self.list_industries = QListWidget()
        self.list_industries.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_industries)

        self.industries_count_label = QLabel("")
        self.industries_count_label.setAlignment(Qt.AlignCenter)
        self.industries_count_label.setStyleSheet("color: #888; margin-top: 5px;")
        layout.addWidget(self.industries_count_label)

        return widget

    def _setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&Файл")

        exit_action = QAction("В&ыход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu("&Вид")

        dashboard_action = QAction("Дашборд", self)
        dashboard_action.setShortcut("Ctrl+0")
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)

        persons_action = QAction("&Люди", self)
        persons_action.setShortcut("Ctrl+1")
        persons_action.triggered.connect(self.show_persons)
        view_menu.addAction(persons_action)

        organizations_action = QAction("&Организации", self)
        organizations_action.setShortcut("Ctrl+2")
        organizations_action.triggered.connect(self.show_organizations)
        view_menu.addAction(organizations_action)

        industries_action = QAction("&Сферы", self)
        industries_action.setShortcut("Ctrl+3")
        industries_action.triggered.connect(self.show_industries)
        view_menu.addAction(industries_action)

    # ============================================================
    # Методы для отображения страниц
    # ============================================================

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.page_dashboard)

    def show_persons(self):
        self.stacked_widget.setCurrentWidget(self.page_persons)
        self._load_persons()

    def show_organizations(self):
        self.stacked_widget.setCurrentWidget(self.page_organizations)
        self._load_organizations()

    def show_industries(self):
        self.stacked_widget.setCurrentWidget(self.page_industries)
        self._load_industries()

    def show_graph(self):
        # TODO: реализовать визуализацию графа
        print("🕸️ Визуализация графа (в разработке)")

    # ============================================================
    # Методы для загрузки данных
    # ============================================================

    def _load_persons(self):
        self.list_persons.clear()
        try:
            persons = get_all_persons(self.session)
            for person in persons:
                display_name = person.full_name or ''
                gender_icon = person.gender_icon if person.gender else ''
                if gender_icon:
                    display_name = f"{gender_icon} {display_name}"

                item = QListWidgetItem(display_name)

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

            self.persons_count_label.setText(f"👤 Всего: {len(persons)} человек")
        except Exception as e:
            self.list_persons.addItem(f"❌ Ошибка загрузки: {e}")
            self.persons_count_label.setText("")

    def _load_organizations(self):
        self.list_organizations.clear()
        try:
            organizations = get_all_organizations(self.session)
            for org in organizations:
                item = QListWidgetItem(f"🏢 {org.name}")
                if org.full_name:
                    item.setText(f"{org.name} ({org.full_name})")
                self.list_organizations.addItem(item)

            self.orgs_count_label.setText(f"🏢 Всего: {len(organizations)} организаций")
        except Exception as e:
            self.list_organizations.addItem(f"❌ Ошибка загрузки: {e}")
            self.orgs_count_label.setText("")

    def _load_industries(self):
        self.list_industries.clear()
        try:
            industries = get_all_industries(self.session)
            for industry in industries:
                item = QListWidgetItem(f"📊 {industry.name}")
                if industry.description:
                    item.setText(f"{industry.name} — {industry.description}")
                self.list_industries.addItem(item)

            self.industries_count_label.setText(f"📊 Всего: {len(industries)} сфер")
        except Exception as e:
            self.list_industries.addItem(f"❌ Ошибка загрузки: {e}")
            self.industries_count_label.setText("")

    def closeEvent(self, event):
        self.session.close()
        event.accept()


# ============================================================
# Точка входа
# ============================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()