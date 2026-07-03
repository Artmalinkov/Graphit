# src/gui/organizations_window.py
"""
Окно со списком организаций
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.work_db.crud import get_all_organizations


class OrganizationsWindow(QWidget):
    """Окно со списком организаций"""

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Организации — Graphite")
        self.setMinimumSize(500, 400)

        self._setup_ui()
        self._load_organizations()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок
        header_layout = QHBoxLayout()

        title = QLabel("🏢 Организации")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)

        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self._load_organizations)
        header_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        # Список
        self.list_organizations = QListWidget()
        self.list_organizations.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #e8f5e9;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
        layout.addWidget(self.list_organizations)

    def _load_organizations(self):
        """Загружает организации из БД"""
        self.list_organizations.clear()
        try:
            organizations = get_all_organizations(self.session)
            for org in organizations:
                display_name = f"🏢 {org.name}"
                if org.full_name:
                    display_name = f"{display_name} ({org.full_name})"
                if org.industry:
                    display_name = f"{display_name} — {org.industry}"

                item = QListWidgetItem(display_name)
                self.list_organizations.addItem(item)

            if organizations:
                self.list_organizations.addItem(f"\n📊 Всего: {len(organizations)} организаций")
        except Exception as e:
            self.list_organizations.addItem(f"❌ Ошибка загрузки: {e}")