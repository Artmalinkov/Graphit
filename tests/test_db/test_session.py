# tests/test_db/test_session.py
"""
Тесты для модуля session.py
"""

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.work_db.session import DatabaseManager, get_engine, get_session, SessionLocal


class TestDatabaseManager:
    """Тесты для класса DatabaseManager"""

    def test_get_engine_returns_engine(self, reset_database_manager, mock_config):
        """
        Проверяет, что get_engine() возвращает объект Engine
        """
        engine = DatabaseManager.get_engine()

        assert isinstance(engine, Engine)
        assert engine is not None

    def test_get_engine_lazy_initialization(self, reset_database_manager, mock_config):
        """
        Проверяет, что Engine создаётся только при первом вызове (ленивая инициализация)
        """
        assert DatabaseManager._engine is None

        engine1 = DatabaseManager.get_engine()
        assert DatabaseManager._engine is not None
        assert isinstance(engine1, Engine)

        engine2 = DatabaseManager.get_engine()
        assert engine1 is engine2

    def test_get_engine_uses_config_url(self, reset_database_manager, mock_config):
        """
        Проверяет, что engine использует URL из конфигурации
        """
        engine = DatabaseManager.get_engine()
        # Проверяем, что используется тестовая БД (не реальная)
        assert 'test.db' in str(engine.url) or ':memory:' in str(engine.url)

    def test_get_session_local_returns_sessionmaker(self, reset_database_manager, mock_config):
        """
        Проверяет, что get_session_local() возвращает фабрику сессий (sessionmaker)
        """
        session_local = DatabaseManager.get_session_local()

        assert isinstance(session_local, sessionmaker)

        session = session_local()
        assert isinstance(session, Session)
        session.close()

    def test_get_session_returns_session(self, reset_database_manager, mock_config):
        """
        Проверяет, что get_session() возвращает объект Session
        """
        session = DatabaseManager.get_session()

        assert isinstance(session, Session)
        assert session is not None
        assert session.is_active
        session.close()

    def test_close_engine_disposes_engine(self, reset_database_manager, mock_config):
        """
        Проверяет, что close_engine() закрывает соединение и сбрасывает состояние
        """
        engine = DatabaseManager.get_engine()
        assert DatabaseManager._engine is not None

        DatabaseManager.close_engine()

        assert DatabaseManager._engine is None
        assert DatabaseManager._session_local is None

    def test_singleton_engine(self, reset_database_manager, mock_config):
        """
        Проверяет, что Engine создаётся в единственном экземпляре (Singleton)
        """
        engine1 = DatabaseManager.get_engine()
        engine2 = DatabaseManager.get_engine()
        engine3 = DatabaseManager.get_engine()

        assert engine1 is engine2
        assert engine2 is engine3

    def test_session_local_is_bound_to_engine(self, reset_database_manager, mock_config):
        """
        Проверяет, что фабрика сессий привязана к правильному engine
        """
        engine = DatabaseManager.get_engine()
        session_local = DatabaseManager.get_session_local()

        assert session_local.kw['bind'] is engine


class TestHelperFunctions:
    """Тесты для вспомогательных функций"""

    def test_get_engine_helper(self, reset_database_manager, mock_config):
        """
        Проверяет, что функция get_engine() работает и возвращает тот же объект
        """
        engine1 = get_engine()
        engine2 = get_engine()

        assert isinstance(engine1, Engine)
        assert engine1 is engine2
        assert engine1 is DatabaseManager.get_engine()

    def test_get_session_helper(self, reset_database_manager, mock_config):
        """
        Проверяет, что функция get_session() работает
        """
        session = get_session()
        try:
            assert isinstance(session, Session)
            assert session.is_active
        finally:
            session.close()

    def test_session_local_helper(self, reset_database_manager, mock_config):
        """
        Проверяет, что SessionLocal — это sessionmaker
        """
        session = SessionLocal()()
        try:
            assert isinstance(session, Session)
        finally:
            session.close()


class TestDatabaseIntegration:
    """Интеграционные тесты — проверяем работу с реальной БД (в памяти)"""

    def test_can_create_and_query_session(self, reset_database_manager, mock_config):
        """
        Проверяет, что через сессию можно выполнять запросы
        """
        session = DatabaseManager.get_session()
        try:
            session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
            session.execute(text("INSERT INTO test (name) VALUES ('test')"))
            session.commit()

            result = session.execute(text("SELECT name FROM test")).fetchone()
            assert result[0] == 'test'
        finally:
            session.close()

    def test_session_rollback_works(self, reset_database_manager, mock_config):
        """
        Проверяет, что откат транзакции работает
        """
        session = DatabaseManager.get_session()
        try:
            session.execute(text("CREATE TABLE test2 (id INTEGER PRIMARY KEY, name TEXT)"))
            session.execute(text("INSERT INTO test2 (name) VALUES ('test1')"))
            session.commit()

            count_before = session.execute(text("SELECT COUNT(*) FROM test2")).fetchone()[0]
            assert count_before == 1

            session.execute(text("INSERT INTO test2 (name) VALUES ('test2')"))
            session.rollback()

            count_after = session.execute(text("SELECT COUNT(*) FROM test2")).fetchone()[0]
            assert count_after == 1
        finally:
            session.close()


class TestEdgeCases:
    """Тесты для краевых случаев"""

    def test_get_session_without_engine(self, reset_database_manager):
        """
        Проверяет, что get_session() работает даже если engine не создан
        (должен создать его автоматически)
        """
        assert DatabaseManager._engine is None

        session = DatabaseManager.get_session()
        try:
            assert DatabaseManager._engine is not None
        finally:
            session.close()

    def test_multiple_close_engine_calls(self, reset_database_manager, mock_config):
        """
        Проверяет, что повторные вызовы close_engine() не вызывают ошибок
        """
        DatabaseManager.get_engine()

        DatabaseManager.close_engine()
        DatabaseManager.close_engine()
        DatabaseManager.close_engine()

        assert DatabaseManager._engine is None
        assert DatabaseManager._session_local is None