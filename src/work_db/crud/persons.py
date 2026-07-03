# src/work_db/crud/persons.py
'''
CRUD-операции для таблицы persons
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Person, Gender
from .base import BaseCRUD

# Создаём экземпляр CRUD для Person
person_crud = BaseCRUD(Person)


def create_person(session: Session, data: Dict[str, Any]) -> Person:
    """
    Создаёт нового человека

    Args:
        session: Сессия SQLAlchemy
        data: Словарь с данными человека
            - full_name: Полное имя (обязательно)
            - family_name: Фамилия
            - name: Имя
            - father_name: Отчество
            - birth_date: Дата рождения
            - gender: Пол (Gender.MALE или Gender.FEMALE)
            - notes: Заметки

    Returns:
        Person: Созданный объект
    """
    # Обрабатываем поле gender
    gender = data.get('gender')
    if gender is not None:
        if isinstance(gender, str):
            try:
                gender = Gender(gender.lower())
            except ValueError:
                gender = None
        elif not isinstance(gender, Gender):
            gender = None

    person = Person(
        full_name=data.get('full_name'),
        family_name=data.get('family_name'),
        name=data.get('name'),
        father_name=data.get('father_name'),
        birth_date=data.get('birth_date'),
        gender=gender,
        notes=data.get('notes')
    )
    session.add(person)
    session.flush()
    return person


def get_person_by_id(session: Session, person_id: int) -> Optional[Person]:
    """Находит человека по ID"""
    return person_crud.get_by_id(session, person_id)


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
    query = session.query(Person).filter_by(family_name=family_name, name=name)
    if father_name:
        query = query.filter_by(father_name=father_name)
    return query.first()


def get_all_persons(session: Session) -> List[Person]:
    """Возвращает всех людей"""
    return person_crud.get_all(session)

def get_persons_by_gender(session: Session, gender: Gender) -> List[Person]:
    """Возвращает людей по полу"""
    return session.query(Person).filter_by(gender=gender).all()

def get_persons_with_gender(session: Session) -> List[Person]:
    """Возвращает людей, у которых указан пол"""
    return session.query(Person).filter(Person.gender.isnot(None)).all()

def get_persons_without_gender(session: Session) -> List[Person]:
    """Возвращает людей, у которых не указан пол"""
    return session.query(Person).filter(Person.gender.is_(None)).all()


def search_persons(session: Session, query: str) -> List[Person]:
    """Ищет людей по полному имени, имени или фамилии"""
    if not query:
        return []

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

    # Обновляем текстовые поля
    updatable_fields = ['full_name', 'family_name', 'name', 'father_name', 'birth_date', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(person, field, data[field])

    # Обновляем поле gender
    if 'gender' in data:
        gender_val = data['gender']
        if gender_val is None:
            person.gender = None
        elif isinstance(gender_val, str):
            try:
                person.gender = Gender(gender_val.lower())
            except ValueError:
                person.gender = None
        elif isinstance(gender_val, Gender):
            person.gender = gender_val
        else:
            person.gender = None

    session.flush()
    return person


def delete_person(session: Session, person_id: int) -> bool:
    """Удаляет человека"""
    return person_crud.delete(session, person_id)

