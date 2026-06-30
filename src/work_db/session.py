'''
Модуль управлениями сессиями в подключении
'''
# src/work_db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import config


class DatabaseManager:
    """Менеджер подключения к БД"""

    _engine = None
    _session_local = None

    @classmethod
    def get_engine(cls):
        """Возвращает engine (ленивая инициализация)"""
        if cls._engine is None:
            cls._engine = create_engine(
                config.DATABASE_URL,
                echo=False,
                pool_pre_ping=True,
            )
        return cls._engine

    @classmethod
    def get_session_local(cls):
        """Возвращает фабрику сессий"""
        if cls._session_local is None:
            cls._session_local = sessionmaker(
                bind=cls.get_engine(),
                autocommit=False,
                autoflush=False,
            )
        return cls._session_local

    @classmethod
    def get_session(cls) -> Session:
        """Создаёт и возвращает новую сессию"""
        return cls.get_session_local()()

    @classmethod
    def close_engine(cls):
        """Закрывает engine (при завершении работы)"""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_local = None


# Упрощённый доступ для быстрого использования
def get_engine():
    return DatabaseManager.get_engine()


def get_session():
    return DatabaseManager.get_session()


SessionLocal = DatabaseManager.get_session_local