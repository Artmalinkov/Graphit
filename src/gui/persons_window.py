# src/gui/persons_window.py
"""
Окно со списком людей
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.work_db.crud import get_all_persons
from src.models import Gender


class PersonsWindow(QWidget):
    """Окно со списком людей"""

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Люди — Graphite")
        self.setMinimumSize(500, 400)

        self._setup_ui()
        self._load_persons()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Заголовок
        header_layout = QHBoxLayout()

        title = QLabel("👤 Люди")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)

        # Кнопка обновления
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self._load_persons)
        header_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        # Список
        self.list_persons = QListWidget()
        self.list_persons.setStyleSheet("""
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
        layout.addWidget(self.list_persons)

    def _load_persons(self):
        """Загружает людей из БД"""
        self.list_persons.clear()
        try:
            persons = get_all_persons(self.session)
            for person in persons:
                display_name = person.full_name or ''
                gender_icon = person.gender_icon if person.gender else ''
                if gender_icon:
                    display_name = f"{gender_icon} {display_name}"

                info = []
                if person.birth_date:
                    info.append(f"р. {person.birth_date.strftime('%d.%m.%Y')}")
                if person.gender:
                    info.append(f"пол: {person.gender_display}")
                if person.notes:
                    info.append(f"📝 {person.notes[:30]}...")

                if info:
                    display_name = f"{display_name} ({' | '.join(info)})"

                item = QListWidgetItem(display_name)
                self.list_persons.addItem(item)

            if persons:
                self.list_persons.addItem(f"\n📊 Всего: {len(persons)} человек")
        except Exception as e:
            self.list_persons.addItem(f"❌ Ошибка загрузки: {e}")