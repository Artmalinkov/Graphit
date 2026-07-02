# src/work_db/crud/entity_types.py
'''
CRUD-операции для таблицы entity_types
'''

from typing import Optional, List
from sqlalchemy.orm import Session

from src.models import EntityType


def get_or_create_entity_type(
    session: Session,
    name: str,
    description: Optional[str] = None
) -> EntityType:
    '''Получает или создаёт тип сущности'''
    entity_type = session.query(EntityType).filter_by(name=name).first()
    if not entity_type:
        entity_type = EntityType(
            name=name,
            description=description or f"Тип: {name}",
            is_active=True
        )
        session.add(entity_type)
        session.flush()
    return entity_type


def get_entity_type_by_name(session: Session, name: str) -> Optional[EntityType]:
    """Получает тип сущности по имени"""
    return session.query(EntityType).filter_by(name=name).first()


def get_all_entity_types(session: Session) -> List[EntityType]:
    """Получает все активные типы сущностей"""
    return session.query(EntityType).filter_by(is_active=True).all()


def get_all_entity_types_including_inactive(session: Session) -> List[EntityType]:
    """Получает все типы сущностей (включая неактивные)"""
    return session.query(EntityType).all()


def update_entity_type(
    session: Session,
    name: str,
    description: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[EntityType]:
    """Обновляет тип сущности"""
    entity_type = get_entity_type_by_name(session, name)
    if not entity_type:
        return None
    if description is not None:
        entity_type.description = description
    if is_active is not None:
        entity_type.is_active = is_active
    session.flush()
    return entity_type


def delete_entity_type(session: Session, name: str) -> bool:
    """Удаляет тип сущности"""
    entity_type = get_entity_type_by_name(session, name)
    if not entity_type:
        return False
    session.delete(entity_type)
    session.flush()
    return True