# src/scripts/db/seed_data.py
"""
Модуль для заполнения базы тестовыми данными
"""

import random
from datetime import datetime
from sqlalchemy.orm import Session

from src.work_db.session import get_session
from src.work_db.crud import (
    create_person,
    create_organization,
    create_industry,
    create_phone,
    create_email,
    create_telegram,
    create_hobby,
    create_connection,
)
from src.models import Person, Organization, Industry, Connection

# ... остальной код без изменений ...

def main():
    """Основная функция для запуска скрипта"""
    session = get_session()
    try:
        seed_database(session, clear_first=True)
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    main()