# src/gui/main_window.py
"""
Главное окно приложения Graphite — дашборд (адаптивный)
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame,
    QStackedWidget, QListWidget, QListWidgetItem,
    QSizePolicy
)
from PySide6.QtCore import Qt, QSize
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
        self.setMinimumSize(600, 650)  # 👈 Увеличено до 600

        self.session = get_session()

        self._setup_ui()
        self._setup_menu()

        self.show_dashboard()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 20)  # 👈 Увеличены отступы по бокам
        self.main_layout.setSpacing(12)

        # ---- Заголовок ----
        header = QLabel("Graphite")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Bold))
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(header)

        subtitle = QLabel("Визуализация социальных связей")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: #888;")
        subtitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(subtitle)

        self.main_layout.addSpacing(15)

        # ---- Стек для переключения контента ----
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.stacked_widget)

        # Создаём страницы
        self.page_dashboard = self._create_dashboard_page()
        self.page_persons = self._create_persons_page()
        self.page_organizations = self._create_organizations_page()
        self.page_industries = self._create_industries_page()

        self.stacked_widget.addWidget(self.page_dashboard)
        self.stacked_widget.addWidget(self.page_persons)
        self.stacked_widget.addWidget(self.page_organizations)
        self.stacked_widget.addWidget(self.page_industries)

    def _create_primary_card(self, title: str, callback):
        """Создаёт большую карточку (Граф) — центрированная, растягивается"""
        card = QPushButton()
        card.setMinimumHeight(100)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 14px;
                padding: 18px 24px;
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

        layout = QVBoxLayout(card)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        layout.addLayout(title_layout)

        return card

    def _create_small_card(self, title: str, callback):
        """
        Создаёт маленькую карточку — центрированная, растягивается,
        БЕЗ ограничения максимальной ширины
        """
        card = QPushButton()
        card.setMinimumHeight(55)
        # Убираем ограничение ширины — карточка будет растягиваться до ширины окна
        # card.setMaximumWidth(800)  # 👈 ЗАКОММЕНТИРОВАНО
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        return card

    def _create_dashboard_page(self):
        """Создаёт страницу дашборда"""
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        # ---- Карточка "Граф" (большая) ----
        card_graph = self._create_primary_card("Граф", self.show_graph)
        layout.addWidget(card_graph)

        layout.addSpacing(10)

        # ---- Маленькие карточки (БЕЗ центрирования, чтобы растягивались) ----
        card_persons = self._create_small_card("Люди", self.show_persons)
        layout.addWidget(card_persons)  # Убрал alignment=Qt.AlignCenter

        card_orgs = self._create_small_card("Организации", self.show_organizations)
        layout.addWidget(card_orgs)

        card_industries = self._create_small_card("Сферы", self.show_industries)
        layout.addWidget(card_industries)

        layout.addSpacing(10)

        # ---- Статус базы данных ----
        status_frame = QFrame()
        status_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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
        status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_label)

        layout.addWidget(status_frame)

        layout.addStretch()

        return widget

    def _create_persons_page(self):
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        back_btn = QPushButton("← Назад")
        back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("👤 Список людей")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header_layout.addWidget(title)

        layout.addLayout(header_layout)

        self.list_persons = QListWidget()
        self.list_persons.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_persons.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
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

        self.persons_count_label = QLabel("")
        self.persons_count_label.setAlignment(Qt.AlignCenter)
        self.persons_count_label.setStyleSheet("color: #888; margin-top: 4px; font-size: 11px;")
        self.persons_count_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.persons_count_label)

        return widget

    def _create_organizations_page(self):
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        back_btn = QPushButton("← Назад")
        back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("🏢 Список организаций")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header_layout.addWidget(title)

        layout.addLayout(header_layout)

        self.list_organizations = QListWidget()
        self.list_organizations.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_organizations.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_organizations)

        self.orgs_count_label = QLabel("")
        self.orgs_count_label.setAlignment(Qt.AlignCenter)
        self.orgs_count_label.setStyleSheet("color: #888; margin-top: 4px; font-size: 11px;")
        self.orgs_count_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.orgs_count_label)

        return widget

    def _create_industries_page(self):
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        back_btn = QPushButton("← Назад")
        back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        back_btn.clicked.connect(self.show_dashboard)
        header_layout.addWidget(back_btn)

        title = QLabel("📊 Список сфер деятельности")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header_layout.addWidget(title)

        layout.addLayout(header_layout)

        self.list_industries = QListWidget()
        self.list_industries.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_industries.setStyleSheet(self.list_persons.styleSheet())
        layout.addWidget(self.list_industries)

        self.industries_count_label = QLabel("")
        self.industries_count_label.setAlignment(Qt.AlignCenter)
        self.industries_count_label.setStyleSheet("color: #888; margin-top: 4px; font-size: 11px;")
        self.industries_count_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.industries_count_label)

        return widget

    def _setup_menu(self):
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
        print("🕸️ Визуализация графа (в разработке)")

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


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()