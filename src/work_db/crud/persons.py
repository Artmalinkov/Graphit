# src/work_db/crud/persons.py
'''
CRUD-операции для таблицы persons
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Person


def create_person(session: Session, data: Dict[str, Any]) -> Person:
    """Создаёт нового человека"""
    person = Person(
        full_name=data.get('full_name'),
        family_name=data.get('family_name'),
        name=data.get('name'),
        father_name=data.get('father_name'),
        birth_date=data.get('birth_date'),
        notes=data.get('notes')
    )
    session.add(person)
    session.flush()
    return person


def get_person_by_id(session: Session, person_id: int) -> Optional[Person]:
    """Находит человека по ID"""
    return session.query(Person).filter_by(id=person_id).first()


def get_person_by_full_name(session: Session, full_name: str) -> Optional[Person]:
    """Находит человека по полному имени"""
    return session.query(Person).filter_by(full_name=full_name).first()


def get_person_by_name_parts(
        session: Session,
        family_name: str,
        name: str,
        father_name: Optional[str] = None
) -> Optional[Person]:
    """Находит человека по частям имени"""
    query = session.query(Person).filter_by(
        family_name=family_name,
        name=name
    )
    if father_name:
        query = query.filter_by(father_name=father_name)
    return query.first()


def get_all_persons(session: Session) -> List[Person]:
    """Возвращает всех людей"""
    return session.query(Person).all()


def search_persons(session: Session, query: str) -> List[Person]:
    """Ищет людей по полному имени, имени или фамилии"""
    search_pattern = f"%{query}%"
    return session.query(Person).filter(
        or_(
            Person.full_name.ilike(search_pattern),
            Person.family_name.ilike(search_pattern),
            Person.name.ilike(search_pattern),
            Person.father_name.ilike(search_pattern),
        )
    ).all()


def update_person(session: Session, person_id: int, data: Dict[str, Any]) -> Optional[Person]:
    """Обновляет данные человека"""
    person = get_person_by_id(session, person_id)
    if not person:
        return None

    updatable_fields = ['full_name', 'family_name', 'name', 'father_name', 'birth_date', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(person, field, data[field])

    session.flush()
    return person


def delete_person(session: Session, person_id: int) -> bool:
    """Удаляет человека по ID"""
    person = get_person_by_id(session, person_id)
    if not person:
        return False
    session.delete(person)
    session.flush()
    return True