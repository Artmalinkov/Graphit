# src/work_db/crud/connections.py
"""
CRUD-операции для таблицы connections
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Connection
from .base import BaseCRUD

# Создаём экземпляр CRUD для Connection
connection_crud = BaseCRUD(Connection)


def get_all_connections(session: Session) -> List[Connection]:
    """Возвращает все связи"""
    return connection_crud.get_all(session)


def create_connection(
        session: Session,
        source_type: str,
        source_id: int,
        target_type: str,
        target_id: int,
        relation_type: str,
        strength: int = 3,
        description: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
) -> Connection:
    """
    Создаёт связь между сущностями
    """
    # Проверяем, существует ли уже такая связь
    existing = session.query(Connection).filter_by(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        relation_type=relation_type
    ).first()

    if existing:
        return existing

    connection = Connection(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        relation_type=relation_type,
        strength=strength,
        description=description,
        attributes=attributes
    )
    session.add(connection)
    session.flush()
    return connection


def get_connection_by_id(session: Session, connection_id: int) -> Optional[Connection]:
    """Находит связь по ID"""
    return connection_crud.get_by_id(session, connection_id)


def get_connections_for_entity(
        session: Session,
        entity_type: str,
        entity_id: int,
        relation_type: Optional[str] = None
) -> List[Connection]:
    """
    Возвращает все связи для сущности
    """
    query = session.query(Connection).filter(
        or_(
            (Connection.source_type == entity_type) & (Connection.source_id == entity_id),
            (Connection.target_type == entity_type) & (Connection.target_id == entity_id),
        )
    )
    if relation_type:
        query = query.filter_by(relation_type=relation_type)
    return query.all()


def get_connections_between(
        session: Session,
        source_type: str,
        source_id: int,
        target_type: str,
        target_id: int,
        relation_type: Optional[str] = None
) -> List[Connection]:
    """
    Возвращает связи между двумя сущностями
    """
    query = session.query(Connection).filter_by(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id
    )
    if relation_type:
        query = query.filter_by(relation_type=relation_type)
    return query.all()


def get_outgoing_connections(
        session: Session,
        entity_type: str,
        entity_id: int,
        relation_type: Optional[str] = None
) -> List[Connection]:
    """
    Возвращает исходящие связи сущности
    """
    query = session.query(Connection).filter_by(
        source_type=entity_type,
        source_id=entity_id
    )
    if relation_type:
        query = query.filter_by(relation_type=relation_type)
    return query.all()


def get_incoming_connections(
        session: Session,
        entity_type: str,
        entity_id: int,
        relation_type: Optional[str] = None
) -> List[Connection]:
    """
    Возвращает входящие связи сущности
    """
    query = session.query(Connection).filter_by(
        target_type=entity_type,
        target_id=entity_id
    )
    if relation_type:
        query = query.filter_by(relation_type=relation_type)
    return query.all()


def update_connection(
        session: Session,
        connection_id: int,
        data: Dict[str, Any]
) -> Optional[Connection]:
    """
    Обновляет связь
    """
    return connection_crud.update(session, connection_id, **data)


def delete_connection(session: Session, connection_id: int) -> bool:
    """
    Удаляет связь по ID
    """
    return connection_crud.delete(session, connection_id)


def delete_connections_for_entity(
        session: Session,
        entity_type: str,
        entity_id: int
) -> int:
    """
    Удаляет все связи для сущности
    """
    connections = get_connections_for_entity(session, entity_type, entity_id)
    count = len(connections)
    for conn in connections:
        session.delete(conn)
    session.flush()
    return count