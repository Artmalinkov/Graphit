# src/gui/graph_window.py
"""
Окно для визуализации графа социальных связей
"""

import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from src.work_db.crud import get_all_persons, get_all_organizations, get_all_connections
from src.graph.builder import build_graph, save_graph_html


class GraphBuilderThread(QThread):
    """Поток для построения графа (чтобы не блокировать интерфейс)"""
    finished = Signal(str)  # Путь к HTML-файлу
    error = Signal(str)  # Сообщение об ошибке
    progress = Signal(int)  # Прогресс 0-100

    def __init__(self, session):
        super().__init__()
        self.session = session

    def run(self):
        try:
            self.progress.emit(10)

            # Загружаем данные
            persons = get_all_persons(self.session)
            self.progress.emit(30)

            organizations = get_all_organizations(self.session)
            self.progress.emit(50)

            connections = get_all_connections(self.session)
            self.progress.emit(70)

            # Строим граф
            G = build_graph(persons, organizations, connections)
            self.progress.emit(85)

            # Сохраняем HTML
            output_path = save_graph_html(G)
            self.progress.emit(100)

            self.finished.emit(str(output_path))
        except Exception as e:
            self.error.emit(str(e))


class GraphWindow(QWidget):
    """Окно с визуализацией графа"""

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Граф связей — Graphite")
        self.setMinimumSize(600, 500)

        self._setup_ui()
        self._build_graph()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ---- Заголовок ----
        header_layout = QHBoxLayout()

        title = QLabel("🕸️ Граф социальных связей")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)

        # Кнопка обновления
        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setFixedWidth(120)
        self.refresh_btn.clicked.connect(self._build_graph)
        header_layout.addWidget(self.refresh_btn, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        # ---- Статус ----
        self.status_label = QLabel("⏳ Построение графа...")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)

        # ---- Прогресс-бар ----
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # ---- Информация ----
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.info_label)

        # ---- Лог ----
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.log_text)

        # ---- Кнопка открытия в браузере ----
        self.open_btn = QPushButton("🌐 Открыть граф в браузере")
        self.open_btn.setFixedHeight(40)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666;
            }
        """)
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self._open_in_browser)
        layout.addWidget(self.open_btn)

        # ---- Кнопка закрытия ----
        close_btn = QPushButton("Закрыть")
        close_btn.setFixedHeight(35)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def _build_graph(self):
        """Запускает построение графа в отдельном потоке"""
        # Блокируем кнопки
        self.refresh_btn.setEnabled(False)
        self.open_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("⏳ Построение графа...")
        self.log_text.clear()
        self.log_text.append("🚀 Начало построения графа...")

        # Запускаем поток
        self.thread = GraphBuilderThread(self.session)
        self.thread.progress.connect(self._update_progress)
        self.thread.finished.connect(self._on_finished)
        self.thread.error.connect(self._on_error)
        self.thread.start()

    def _update_progress(self, value):
        """Обновляет прогресс-бар"""
        self.progress_bar.setValue(value)
        if value < 30:
            self.log_text.append("📂 Загрузка данных...")
        elif value < 50:
            self.log_text.append("📊 Построение узлов графа...")
        elif value < 70:
            self.log_text.append("🔗 Построение связей...")
        elif value < 85:
            self.log_text.append("🎨 Формирование визуализации...")
        else:
            self.log_text.append("💾 Сохранение HTML...")

    def _on_finished(self, html_path):
        """Обработка завершения построения"""
        self.progress_bar.setValue(100)
        self.status_label.setText("✅ Граф построен!")
        self.refresh_btn.setEnabled(True)
        self.open_btn.setEnabled(True)
        self.log_text.append(f"✅ Граф сохранён: {html_path}")

        # Показываем информацию о графе
        from src.graph.builder import get_graph_info
        info = get_graph_info(html_path)
        if info:
            self.info_label.setText(
                f"📊 Узлов: {info.get('nodes', 0)}, "
                f"Рёбер: {info.get('edges', 0)}"
            )

    def _on_error(self, error_msg):
        """Обработка ошибки"""
        self.progress_bar.setValue(0)
        self.status_label.setText("❌ Ошибка построения графа")
        self.refresh_btn.setEnabled(True)
        self.open_btn.setEnabled(False)
        self.log_text.append(f"❌ Ошибка: {error_msg}")

    def _open_in_browser(self):
        """Открывает HTML-файл в браузере"""
        html_path = Path("output/graph.html")
        if html_path.exists():
            webbrowser.open(str(html_path.absolute()))
            self.log_text.append(f"🌐 Открыт в браузере: {html_path}")
        else:
            self.log_text.append("❌ Файл не найден. Попробуйте построить граф заново.")