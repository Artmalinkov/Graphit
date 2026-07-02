# src/work_db/crud/telegrams.py
"""
CRUD-операции для таблицы telegrams
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from src.models import Telegram


def create_telegram(session: Session, data: Dict[str, Any]) -> Telegram:
    """Создаёт Telegram-аккаунт"""
    telegram = Telegram(
        username=data.get('username'),
        type=data.get('type', 'personal'),
        is_primary=data.get('is_primary', False),
        notes=data.get('notes')
    )
    session.add(telegram)
    session.flush()
    return telegram


def get_telegram_by_id(session: Session, telegram_id: int) -> Optional[Telegram]:
    """Находит Telegram по ID"""
    return session.query(Telegram).filter_by(id=telegram_id).first()


def get_telegram_by_username(session: Session, username: str) -> Optional[Telegram]:
    """Находит Telegram по username"""
    return session.query(Telegram).filter_by(username=username).first()


def get_all_telegrams(session: Session) -> List[Telegram]:
    """Возвращает все Telegram-аккаунты"""
    return session.query(Telegram).all()


def search_telegrams(session: Session, query: str) -> List[Telegram]:
    """Ищет Telegram по username"""
    search_pattern = f"%{query}%"
    return session.query(Telegram).filter(Telegram.username.ilike(search_pattern)).all()


def update_telegram(session: Session, telegram_id: int, data: Dict[str, Any]) -> Optional[Telegram]:
    """Обновляет Telegram"""
    telegram = get_telegram_by_id(session, telegram_id)
    if not telegram:
        return None

    updatable_fields = ['username', 'type', 'is_primary', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(telegram, field, data[field])

    session.flush()
    return telegram


def delete_telegram(session: Session, telegram_id: int) -> bool:
    """Удаляет Telegram"""
    telegram = get_telegram_by_id(session, telegram_id)
    if not telegram:
        return False
    session.delete(telegram)
    session.flush()
    return True