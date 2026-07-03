# src/gui/industries_window.py
"""
Окно со списком сфер деятельности
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.work_db.crud import get_all_industries


class IndustriesWindow(QWidget):
    """Окно со списком сфер деятельности"""

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Сферы деятельности — Graphite")
        self.setMinimumSize(500, 400)

        self._setup_ui()
        self._load_industries()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок
        header_layout = QHBoxLayout()

        title = QLabel("📊 Сферы деятельности")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)

        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self._load_industries)
        header_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        # Список
        self.list_industries = QListWidget()
        self.list_industries.setStyleSheet("""
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
        layout.addWidget(self.list_industries)

    def _load_industries(self):
        """Загружает сферы деятельности из БД"""
        self.list_industries.clear()
        try:
            industries = get_all_industries(self.session)
            for industry in industries:
                display_name = f"📊 {industry.name}"
                if industry.description:
                    display_name = f"{display_name} — {industry.description}"

                item = QListWidgetItem(display_name)
                self.list_industries.addItem(item)

            if industries:
                self.list_industries.addItem(f"\n📊 Всего: {len(industries)} сфер")
        except Exception as e:
            self.list_industries.addItem(f"❌ Ошибка загрузки: {e}")