# src/scripts/db/__init__.py
"""Скрипты для управления базой данных"""

from .seed_data import seed_database
from .clear_data import clear_database

__all__ = [
    'seed_database',
    'clear_database',
]