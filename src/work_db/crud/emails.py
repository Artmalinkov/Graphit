# src/work_db/crud/emails.py
"""
CRUD-операции для таблицы emails
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from src.models import Email


def create_email(session: Session, data: Dict[str, Any]) -> Email:
    """Создаёт email"""
    email = Email(
        address=data.get('address'),
        type=data.get('type', 'personal'),
        is_primary=data.get('is_primary', False),
        notes=data.get('notes')
    )
    session.add(email)
    session.flush()
    return email


def get_email_by_id(session: Session, email_id: int) -> Optional[Email]:
    """Находит email по ID"""
    return session.query(Email).filter_by(id=email_id).first()


def get_email_by_address(session: Session, address: str) -> Optional[Email]:
    """Находит email по адресу"""
    return session.query(Email).filter_by(address=address).first()


def get_all_emails(session: Session) -> List[Email]:
    """Возвращает все email"""
    return session.query(Email).all()


def search_emails(session: Session, query: str) -> List[Email]:
    """Ищет email по адресу"""
    search_pattern = f"%{query}%"
    return session.query(Email).filter(Email.address.ilike(search_pattern)).all()


def update_email(session: Session, email_id: int, data: Dict[str, Any]) -> Optional[Email]:
    """Обновляет email"""
    email = get_email_by_id(session, email_id)
    if not email:
        return None

    updatable_fields = ['address', 'type', 'is_primary', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(email, field, data[field])

    session.flush()
    return email


def delete_email(session: Session, email_id: int) -> bool:
    """Удаляет email"""
    email = get_email_by_id(session, email_id)
    if not email:
        return False
    session.delete(email)
    session.flush()
    return True