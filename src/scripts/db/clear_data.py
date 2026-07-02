# src/scripts/db/clear_data.py
"""
Скрипт для очистки базы данных
"""

import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.work_db.session import get_session
from src.models import (
    Person, Organization, Industry, Connection,
    Phone, Email, Telegram, Hobby, Address
)


def clear_database(session, confirm=True):
    """
    Очищает все таблицы базы данных

    Args:
        session: Сессия SQLAlchemy
        confirm: Запрашивать подтверждение
    """
    if confirm:
        response = input("⚠️ Вы уверены, что хотите очистить все данные? (y/n): ")
        if response.lower() != 'y':
            print("❌ Очистка отменена")
            return False

    print("🧹 Очистка базы данных...")

    # Удаляем в порядке зависимости (сначала дочерние)
    session.query(Connection).delete()
    session.query(Person).delete()
    session.query(Organization).delete()
    session.query(Industry).delete()
    session.query(Phone).delete()
    session.query(Email).delete()
    session.query(Telegram).delete()
    session.query(Hobby).delete()
    session.query(Address).delete()

    session.commit()
    print("✅ База данных очищена")
    return True


def main():
    """Основная функция"""
    session = get_session()
    try:
        clear_database(session, confirm=True)
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка при очистке: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    main()