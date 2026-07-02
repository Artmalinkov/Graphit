# src/work_db/crud/hobbies.py
"""
CRUD-операции для таблицы hobbies
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Hobby


def create_hobby(session: Session, data: Dict[str, Any]) -> Hobby:
    """Создаёт хобби"""
    hobby = Hobby(
        name=data.get('name'),
        category=data.get('category'),
        description=data.get('description')
    )
    session.add(hobby)
    session.flush()
    return hobby


def get_hobby_by_id(session: Session, hobby_id: int) -> Optional[Hobby]:
    """Находит хобби по ID"""
    return session.query(Hobby).filter_by(id=hobby_id).first()


def get_hobby_by_name(session: Session, name: str) -> Optional[Hobby]:
    """Находит хобби по названию"""
    return session.query(Hobby).filter_by(name=name).first()


def get_all_hobbies(session: Session) -> List[Hobby]:
    """Возвращает все хобби"""
    return session.query(Hobby).all()


def search_hobbies(session: Session, query: str) -> List[Hobby]:
    """Ищет хобби по названию или категории"""
    search_pattern = f"%{query}%"
    return session.query(Hobby).filter(
        or_(
            Hobby.name.ilike(search_pattern),
            Hobby.category.ilike(search_pattern),
        )
    ).all()


def update_hobby(session: Session, hobby_id: int, data: Dict[str, Any]) -> Optional[Hobby]:
    """Обновляет хобби"""
    hobby = get_hobby_by_id(session, hobby_id)
    if not hobby:
        return None

    updatable_fields = ['name', 'category', 'description']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(hobby, field, data[field])

    session.flush()
    return hobby


def delete_hobby(session: Session, hobby_id: int) -> bool:
    """Удаляет хобби"""
    hobby = get_hobby_by_id(session, hobby_id)
    if not hobby:
        return False
    session.delete(hobby)
    session.flush()
    return True