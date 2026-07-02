# src/scripts/db/__init__.py
"""
Скрипты для управления базой данных
"""

from .seed_data import seed_database
from .clear_data import clear_database
from .test_data import (
    PEOPLE,
    ORGANIZATIONS,
    INDUSTRIES,
    PHONES,
    EMAILS,
    TELEGRAMS,
    HOBBIES,
    get_connection_data,
)

__all__ = [
    'seed_database',
    'clear_database',
    'PEOPLE',
    'ORGANIZATIONS',
    'INDUSTRIES',
    'PHONES',
    'EMAILS',
    'TELEGRAMS',
    'HOBBIES',
    'get_connection_data',
]