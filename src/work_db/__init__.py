# src/work_db/__init__.py
from .session import get_session, get_engine, SessionLocal
from .crud import *

# Добавляем Gender в экспорт
from src.models import Gender

__all__ = [
    # Session
    'get_session',
    'get_engine',
    'SessionLocal',

    # Enums
    'Gender',

    # CRUD
    'create_person',
    'get_person_by_name',
    'get_all_persons',
    'create_phone',
    'create_email',
    'create_telegram',
    'create_hobby',
    'create_organization',
    'create_address',
    'create_connection',
    'create_industry',
    'get_or_create_entity_type',

    # Queries
    'get_person_with_all_connections',
    'get_all_persons_with_connections',
    'get_connections_graph_data',
]