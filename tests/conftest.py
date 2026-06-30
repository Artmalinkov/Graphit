# tests/conftest.py
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.work_db.session import DatabaseManager


@pytest.fixture(scope="function")
def reset_database_manager():
    """
    Сбрасывает состояние DatabaseManager между тестами.
    Это важно, чтобы тесты не влияли друг на друга.
    """
    # Сохраняем старые значения
    old_engine = DatabaseManager._engine
    old_session_local = DatabaseManager._session_local

    # Сбрасываем
    DatabaseManager._engine = None
    DatabaseManager._session_local = None

    yield

    # Восстанавливаем (на случай, если другие тесты полагаются на состояние)
    DatabaseManager._engine = old_engine
    DatabaseManager._session_local = old_session_local


@pytest.fixture(scope="function")
def mock_config(monkeypatch, tmp_path):
    """
    Подменяет конфигурацию для тестов.
    Использует временную БД вместо реальной.
    """
    # Создаём временный файл БД в папке tmp_path
    test_db_path = tmp_path / "test.db"

    # Подменяем DB_PATH на временный файл
    monkeypatch.setattr('config.config.DB_PATH', str(test_db_path))

    class MockConfig:
        DATABASE_URL = f'sqlite:///{test_db_path}'

    return MockConfig()


@pytest.fixture(scope="function")
def test_engine():
    """
    Создаёт временную БД в памяти для тестов.
    Используется для изоляции тестов друг от друга.
    """
    # Создаём engine для тестовой БД
    engine = create_engine('sqlite:///:memory:')

    # Создаём все таблицы
    Base.metadata.create_all(engine)

    yield engine

    # Очищаем после теста
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Создаёт сессию для тестов"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_md_file():
    """Путь к тестовому .md файлу"""
    return Path(__file__).parent / "fixtures" / "sample_note.md"