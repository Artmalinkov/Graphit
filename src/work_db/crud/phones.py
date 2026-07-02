# src/work_db/crud/phones.py
'''
CRUD-операции для таблицы phones
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from src.models import Phone


def create_phone(session: Session, data: Dict[str, Any]) -> Phone:
    """Создаёт телефон"""
    phone = Phone(
        number=data.get('number'),
        type=data.get('type', 'mobile'),
        is_primary=data.get('is_primary', False),
        notes=data.get('notes')
    )
    session.add(phone)
    session.flush()
    return phone


def get_phone_by_id(session: Session, phone_id: int) -> Optional[Phone]:
    """Находит телефон по ID"""
    return session.query(Phone).filter_by(id=phone_id).first()


def get_phone_by_number(session: Session, number: str) -> Optional[Phone]:
    """Находит телефон по номеру"""
    return session.query(Phone).filter_by(number=number).first()


def get_all_phones(session: Session) -> List[Phone]:
    """Возвращает все телефоны"""
    return session.query(Phone).all()


def search_phones(session: Session, query: str) -> List[Phone]:
    """Ищет телефоны по номеру"""
    search_pattern = f"%{query}%"
    return session.query(Phone).filter(Phone.number.ilike(search_pattern)).all()


def update_phone(session: Session, phone_id: int, data: Dict[str, Any]) -> Optional[Phone]:
    """Обновляет телефон"""
    phone = get_phone_by_id(session, phone_id)
    if not phone:
        return None

    updatable_fields = ['number', 'type', 'is_primary', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(phone, field, data[field])

    session.flush()
    return phone


def delete_phone(session: Session, phone_id: int) -> bool:
    """Удаляет телефон"""
    phone = get_phone_by_id(session, phone_id)
    if not phone:
        return False
    session.delete(phone)
    session.flush()
    return True