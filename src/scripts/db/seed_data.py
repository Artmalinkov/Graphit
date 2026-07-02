# src/scripts/db/seed_data.py
"""
Модуль для заполнения базы тестовыми данными
"""

import random
import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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
from src.models import Person, Organization, Industry, Connection, Phone, Email, Telegram, Hobby

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
from .clear_data import clear_database


# ============================================================
# Основная функция заполнения
# ============================================================

def seed_database(session: Session, clear_first: bool = True):
    """
    Заполняет базу тестовыми данными

    Args:
        session: Сессия SQLAlchemy
        clear_first: Очистить ли базу перед заполнением
    """
    print("=" * 60)
    print("🌱 ЗАПОЛНЕНИЕ БАЗЫ ТЕСТОВЫМИ ДАННЫМИ")
    print("=" * 60)

    if clear_first:
        clear_database(session, confirm=False)

    # Кэши для хранения созданных объектов
    person_cache = {}
    org_cache = {}
    industry_cache = {}
    phone_cache = []
    email_cache = []
    telegram_cache = []
    hobby_cache = {}

    # ============================================================
    # 1. Создаём сферы деятельности
    # ============================================================
    print("\n📊 Создание сфер деятельности...")
    for industry_data in INDUSTRIES:
        industry = create_industry(session, industry_data)
        industry_cache[industry.name] = industry
        print(f"  ✅ {industry.name}")

    # ============================================================
    # 2. Создаём организации
    # ============================================================
    print("\n🏢 Создание организаций...")
    for org_data in ORGANIZATIONS:
        org = create_organization(session, org_data)
        org_cache[org.name] = org
        print(f"  ✅ {org.name}")

    # ============================================================
    # 3. Создаём людей
    # ============================================================
    print("\n👤 Создание людей...")
    for person_data in PEOPLE:
        person = create_person(session, person_data)
        person_cache[person.full_name] = person
        print(f"  ✅ {person.full_name} (пол: {person.gender or 'не указан'})")

    # ============================================================
    # 4. Создаём телефоны и связи с людьми
    # ============================================================
    print("\n📞 Создание телефонов...")
    person_list = list(person_cache.values())
    for i, phone_data in enumerate(PHONES):
        phone = create_phone(session, phone_data)
        phone_cache.append(phone)

        # Распределяем телефоны по людям (по кругу)
        person = person_list[i % len(person_list)]
        create_connection(
            session,
            source_type='person',
            source_id=person.id,
            target_type='phone',
            target_id=phone.id,
            relation_type='has_phone',
            attributes={'type': phone_data['type'], 'is_primary': phone_data['is_primary']}
        )
        print(f"  ✅ {phone.number} → {person.full_name}")

    # ============================================================
    # 5. Создаём Email и связи с людьми
    # ============================================================
    print("\n📧 Создание Email...")
    for i, email_data in enumerate(EMAILS):
        email = create_email(session, email_data)
        email_cache.append(email)

        person = person_list[i % len(person_list)]
        create_connection(
            session,
            source_type='person',
            source_id=person.id,
            target_type='email',
            target_id=email.id,
            relation_type='has_email',
            attributes={'type': email_data['type'], 'is_primary': email_data['is_primary']}
        )
        print(f"  ✅ {email.address} → {person.full_name}")

    # ============================================================
    # 6. Создаём Telegram и связи с людьми
    # ============================================================
    print("\n💬 Создание Telegram...")
    for i, tg_data in enumerate(TELEGRAMS):
        telegram = create_telegram(session, tg_data)
        telegram_cache.append(telegram)

        person = person_list[i % len(person_list)]
        create_connection(
            session,
            source_type='person',
            source_id=person.id,
            target_type='telegram',
            target_id=telegram.id,
            relation_type='has_telegram',
            attributes={'type': tg_data['type'], 'is_primary': tg_data['is_primary']}
        )
        print(f"  ✅ {telegram.username} → {person.full_name}")

    # ============================================================
    # 7. Создаём Хобби и связи с людьми
    # ============================================================
    print("\n🎯 Создание хобби...")
    for hobby_data in HOBBIES:
        hobby = create_hobby(session, hobby_data)
        hobby_cache[hobby.name] = hobby
        print(f"  ✅ {hobby.name}")

    # Связываем людей с хобби (2-3 хобби на человека)
    print("\n🔗 Связывание людей с хобби...")
    hobby_list = list(hobby_cache.values())
    for person in person_list:
        num_hobbies = random.randint(2, 3)
        selected_hobbies = random.sample(
            hobby_list,
            min(num_hobbies, len(hobby_list))
        )
        for hobby in selected_hobbies:
            create_connection(
                session,
                source_type='person',
                source_id=person.id,
                target_type='hobby',
                target_id=hobby.id,
                relation_type='has_hobby',
                strength=random.randint(3, 5)
            )
        print(f"  ✅ {person.full_name} → {len(selected_hobbies)} хобби")

    # ============================================================
    # 8. Связываем людей с организациями (работа)
    # ============================================================
    print("\n🔗 Связывание людей с организациями...")
    positions = ['Разработчик', 'Дизайнер', 'Менеджер', 'Директор', 'Аналитик', 'Маркетолог']
    org_list = list(org_cache.values())

    for i, person in enumerate(person_list):
        if org_list:
            org = org_list[i % len(org_list)]
            position = random.choice(positions)

            create_connection(
                session,
                source_type='person',
                source_id=person.id,
                target_type='organization',
                target_id=org.id,
                relation_type='works_at',
                strength=random.randint(3, 5),
                attributes={'role': position, 'start_date': datetime.now().strftime('%Y-%m-%d')}
            )
            print(f"  ✅ {person.full_name} → {org.name} ({position})")

    # ============================================================
    # 9. Связываем людей со сферами деятельности
    # ============================================================
    print("\n🔗 Связывание людей со сферами деятельности...")
    industry_list = list(industry_cache.values())
    for person in person_list:
        industry = random.choice(industry_list)
        create_connection(
            session,
            source_type='person',
            source_id=person.id,
            target_type='industry',
            target_id=industry.id,
            relation_type='works_in',
            strength=random.randint(3, 5)
        )
        print(f"  ✅ {person.full_name} → {industry.name}")

    # ============================================================
    # 10. Связываем людей между собой
    # ============================================================
    print("\n🔗 Создание связей между людьми...")
    connection_data = get_connection_data()

    for source_name, target_name, relation_type, strength in connection_data:
        source = person_cache.get(source_name)
        target = person_cache.get(target_name)

        if source and target:
            create_connection(
                session,
                source_type='person',
                source_id=source.id,
                target_type='person',
                target_id=target.id,
                relation_type=relation_type,
                strength=strength,
                description=f'Связь между {source_name} и {target_name}'
            )
            print(f"  ✅ {source_name} → {target_name} ({relation_type})")

    # ============================================================
    # 11. Коммитим все изменения
    # ============================================================
    session.commit()

    # ============================================================
    # 12. Итог
    # ============================================================
    print("\n" + "=" * 60)
    print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 60)
    print(f"  👤 Людей:        {len(person_cache)}")
    print(f"  🏢 Организаций:  {len(org_cache)}")
    print(f"  📊 Сфер:         {len(industry_cache)}")
    print(f"  📞 Телефонов:    {len(phone_cache)}")
    print(f"  📧 Email:        {len(email_cache)}")
    print(f"  💬 Telegram:     {len(telegram_cache)}")
    print(f"  🎯 Хобби:        {len(hobby_cache)}")
    print(f"  🔗 Связей:       {len(connection_data)} (между людьми)")
    print("=" * 60)


# ============================================================
# Точка входа
# ============================================================

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