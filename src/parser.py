# src/parser.py
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from sqlalchemy.orm import Session

from config import config

from src.models import (
    Base, Person, Organization, Address, Phone, Email, Telegram, Hobby,
    Industry, Connection, EntityType
)


# ============================================================
# 1. Парсинг одного .md файла
# ============================================================
def parse_md_file(file_path: Path) -> Dict[str, Any]:
    """
    Парсит один .md файл и извлекает структурированные данные
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Имя файла = имя сущности
    name = file_path.stem

    # Результат
    result = {
        'name': name,
        'type': 'person',  # по умолчанию
        'first_name': None,
        'last_name': None,
        'middle_name': None,
        'birth_date': None,
        'phone': None,
        'email': None,
        'telegram': None,
        'hobbies': [],
        'address': None,
        'organization': None,
        'industry': None,
        'connections': [],  # [(имя, тип_связи)]
        'wiki_links': [],
        'notes': '',
        'raw_text': content
    }

    # ============================================================
    # Ищем все поля в формате Ключ:: Значение
    # ============================================================
    dataview_fields = {}
    for line in content.split('\n'):
        if '::' in line and not line.strip().startswith('-'):
            parts = line.split('::', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            dataview_fields[key] = value

    # ============================================================
    # Извлекаем данные из Dataview-полей
    # ============================================================

    # --- ФИО ---
    fio = dataview_fields.get('ФИО', '')
    if fio:
        parts = fio.split()
        if len(parts) >= 3:
            result['last_name'] = parts[0]
            result['first_name'] = parts[1]
            result['middle_name'] = parts[2]
        elif len(parts) == 2:
            result['last_name'] = parts[0]
            result['first_name'] = parts[1]
        else:
            result['first_name'] = fio

    # --- Дата рождения ---
    birth = dataview_fields.get('Дата_рождения', '')
    if birth:
        result['birth_date'] = birth

    # --- Телефон ---
    phone = dataview_fields.get('Телефон', '')
    if phone:
        result['phone'] = phone

    # --- Email ---
    email = dataview_fields.get('Электронная_почта', '')
    if email:
        result['email'] = email

    # --- Telegram ---
    telegram = dataview_fields.get('Аккаунт_Telegram', '')
    if telegram:
        result['telegram'] = telegram

    # --- Увлечения ---
    hobbies = dataview_fields.get('Увлечения', '')
    if hobbies and hobbies != '-':
        result['hobbies'] = [h.strip() for h in hobbies.split(',') if h.strip()]

    # --- Сфера деятельности ---
    industry = dataview_fields.get('Сфера деятельности', '')
    if industry and industry != '-':
        result['industry'] = industry

    # --- Связь с организацией ---
    org = dataview_fields.get('Связь с юрлицом', '')
    if org and org != '-':
        result['organization'] = org

    # --- Связь с адресом ---
    address = dataview_fields.get('Связь с адресом', '')
    if address and address != '-':
        result['address'] = address

    # --- Связь с физлицами ---
    person_conn = dataview_fields.get('Связь с физлицом', '')
    if person_conn and person_conn != '-':
        for item in person_conn.split(','):
            cleaned = item.strip()
            if cleaned:
                result['connections'].append((cleaned, 'friend'))

    # --- Дополнительные связи ---
    extra = dataview_fields.get('Дополнительно', '')
    if extra and extra != '-':
        for item in extra.split(','):
            cleaned = item.strip()
            if cleaned:
                # Проверяем, есть ли указание типа связи через двоеточие
                if ':' in cleaned:
                    parts = cleaned.split(':', 1)
                    result['connections'].append((parts[1].strip(), parts[0].strip()))
                else:
                    result['connections'].append((cleaned, 'related'))

    # --- Заметки ---
    notes_parts = []

    # Внутренние качества
    qualities = dataview_fields.get('Внутренние качества', '')
    if qualities and qualities != '-':
        notes_parts.append(f"Качества: {qualities}")

    # Примечание
    note = dataview_fields.get('Примечание', '')
    if note and note != '-':
        notes_parts.append(f"Примечание: {note}")

    # Семья
    family = dataview_fields.get('Семья', '')
    if family and family != '-':
        notes_parts.append(f"Семья: {family}")

    # Место знакомства
    place = dataview_fields.get('Место_знакомства', '')
    if place and place != '-':
        notes_parts.append(f"Место знакомства: {place}")

    result['notes'] = '\n'.join(notes_parts)

    # ============================================================
    # Находим все вики-ссылки [[...]]
    # ============================================================
    wiki_links = re.findall(r'\[\[(.*?)(?:\|.*?)?\]\]', content)
    result['wiki_links'] = [link.strip() for link in wiki_links if link.strip()]

    # ============================================================
    # Определяем тип сущности из Frontmatter
    # ============================================================
    # Ищем YAML Frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            # Ищем type
            type_match = re.search(r'type:\s*(.+?)(?:\n|$)', frontmatter_text)
            if type_match:
                type_val = type_match.group(1).strip()
                if type_val in ['person', 'organization', 'company']:
                    result['type'] = type_val

    # Если в связях есть организация, возможно это организация
    if result['organization'] and result['type'] == 'person':
        result['type'] = 'person'  # оставляем person, так как у человека есть связь с организацией

    return result


# ============================================================
# 2. Сканирование папки Obsidian
# ============================================================
def scan_obsidian_folder() -> List[Dict[str, Any]]:
    """Сканирует папку Obsidian и парсит все .md файлы"""
    obsidian_path = config.OBSIDIAN_PATH
    results = []

    if not obsidian_path.exists():
        print(f"❌ Папка не найдена: {obsidian_path}")
        return results

    md_files = list(obsidian_path.rglob('*.md'))
    print(f"🔍 Найдено {len(md_files)} .md файлов")

    for md_file in md_files:
        try:
            parsed = parse_md_file(md_file)
            results.append(parsed)
            print(f"  ✅ {parsed['name']} (тип: {parsed['type']}, связей: {len(parsed['connections'])})")
        except Exception as e:
            print(f"  ❌ Ошибка в {md_file.name}: {e}")

    return results


# ============================================================
# 3. Сохранение в JSON (для отладки)
# ============================================================
def save_to_json(data: List[Dict[str, Any]], filename: str = 'obsidian_dump.json') -> None:
    """Сохраняет результаты парсинга в JSON"""
    output_path = config.DATA_PROCESSED / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Данные сохранены в {output_path}")


# ============================================================
# 4. Загрузка в БД через SQLAlchemy
# ============================================================
def load_to_database(data: List[Dict[str, Any]], session: Session) -> None:
    """Загружает распарсенные данные в базу данных"""

    for item in data:
        print(f"📝 Обработка: {item['name']}")

        # ---- 1. Создаём или находим Person ----
        person = session.query(Person).filter_by(name=item['name']).first()
        if not person:
            person = Person(
                name=item['name'],
                first_name=item.get('first_name'),
                last_name=item.get('last_name'),
                middle_name=item.get('middle_name'),
                notes=item.get('notes')
            )
            session.add(person)
            session.flush()
            print(f"  ✅ Создан Person: {person.name}")
        else:
            print(f"  ℹ️ Person уже существует: {person.name}")

        # ---- 2. Обрабатываем телефон ----
        if item.get('phone'):
            phone = session.query(Phone).filter_by(number=item['phone']).first()
            if not phone:
                phone = Phone(number=item['phone'], type='mobile')
                session.add(phone)
                session.flush()
                print(f"  📞 Создан Phone: {phone.number}")

            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='phone',
                target_id=phone.id,
                relation_type='has_phone'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='phone',
                    target_id=phone.id,
                    relation_type='has_phone',
                    attributes={'type': 'mobile', 'is_primary': True}
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {phone.number}")

        # ---- 3. Обрабатываем Email ----
        if item.get('email'):
            email = session.query(Email).filter_by(address=item['email']).first()
            if not email:
                email = Email(address=item['email'], type='personal')
                session.add(email)
                session.flush()
                print(f"  📧 Создан Email: {email.address}")

            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='email',
                target_id=email.id,
                relation_type='has_email'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='email',
                    target_id=email.id,
                    relation_type='has_email',
                    attributes={'type': 'personal', 'is_primary': True}
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {email.address}")

                # ---- 4. Обрабатываем Telegram ----
                if item.get('telegram'):
                    # Проверяем, есть ли уже такой Telegram
                    telegram = session.query(Telegram).filter_by(username=item['telegram']).first()
                    if not telegram:
                        telegram = Telegram(
                            username=item['telegram'],
                            type='personal',
                            is_primary=True
                        )
                        session.add(telegram)
                        session.flush()
                        print(f"  💬 Создан Telegram: @{telegram.username}")

        # ---- 5. Обрабатываем Хобби ----
        for hobby_name in item.get('hobbies', []):
            hobby = session.query(Hobby).filter_by(name=hobby_name).first()
            if not hobby:
                hobby = Hobby(name=hobby_name)
                session.add(hobby)
                session.flush()
                print(f"  🎯 Создано Hobby: {hobby.name}")

            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='hobby',
                target_id=hobby.id,
                relation_type='has_hobby'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='hobby',
                    target_id=hobby.id,
                    relation_type='has_hobby'
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {hobby.name}")

        # ---- 6. Обрабатываем Сферу деятельности ----
        if item.get('industry'):
            industry = session.query(Industry).filter_by(name=item['industry']).first()
            if not industry:
                industry = Industry(name=item['industry'])
                session.add(industry)
                session.flush()
                print(f"  🏭 Создана Industry: {industry.name}")

            # Связь Person → Industry
            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='industry',
                target_id=industry.id,
                relation_type='works_in'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='industry',
                    target_id=industry.id,
                    relation_type='works_in'
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {industry.name}")

        # ---- 7. Обрабатываем Организацию ----
        if item.get('organization'):
            org = session.query(Organization).filter_by(name=item['organization']).first()
            if not org:
                org = Organization(name=item['organization'])
                session.add(org)
                session.flush()
                print(f"  🏢 Создана Organization: {org.name}")

            # Связь Person → Organization
            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='organization',
                target_id=org.id,
                relation_type='works_at'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='organization',
                    target_id=org.id,
                    relation_type='works_at'
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {org.name}")

        # ---- 8. Обрабатываем связи с другими людьми ----
        for conn_target, relation_type in item.get('connections', []):
            # Ищем цель
            target_person = session.query(Person).filter_by(name=conn_target).first()
            if target_person:
                existing = session.query(Connection).filter_by(
                    source_type='person',
                    source_id=person.id,
                    target_type='person',
                    target_id=target_person.id,
                    relation_type=relation_type
                ).first()
                if not existing:
                    conn = Connection(
                        source_type='person',
                        source_id=person.id,
                        target_type='person',
                        target_id=target_person.id,
                        relation_type=relation_type,
                        strength=3
                    )
                    session.add(conn)
                    print(f"  🔗 Связь {person.name} → {target_person.name} ({relation_type})")

        # ---- 9. Обрабатываем Адрес ----
        if item.get('address'):
            addr = session.query(Address).filter_by(full_address=item['address']).first()
            if not addr:
                addr = Address(full_address=item['address'])
                session.add(addr)
                session.flush()
                print(f"  📍 Создан Address: {addr.full_address[:50]}...")

            existing = session.query(Connection).filter_by(
                source_type='person',
                source_id=person.id,
                target_type='address',
                target_id=addr.id,
                relation_type='lives_at'
            ).first()
            if not existing:
                conn = Connection(
                    source_type='person',
                    source_id=person.id,
                    target_type='address',
                    target_id=addr.id,
                    relation_type='lives_at'
                )
                session.add(conn)
                print(f"  🔗 Связь {person.name} → {addr.full_address[:50]}...")

        # ---- 10. Обрабатываем вики-ссылки как потенциальные связи ----
        for link in item.get('wiki_links', []):
            # Проверяем, есть ли такой человек в БД
            target_person = session.query(Person).filter_by(name=link).first()
            if target_person and target_person.id != person.id:
                existing = session.query(Connection).filter_by(
                    source_type='person',
                    source_id=person.id,
                    target_type='person',
                    target_id=target_person.id,
                    relation_type='mentioned'
                ).first()
                if not existing:
                    conn = Connection(
                        source_type='person',
                        source_id=person.id,
                        target_type='person',
                        target_id=target_person.id,
                        relation_type='mentioned',
                        strength=1,
                        description='Упоминание в заметке'
                    )
                    session.add(conn)
                    print(f"  🔗 Упоминание: {person.name} → {target_person.name}")

        # Коммитим после каждого человека
        session.commit()

    print("\n✅ Все данные загружены!")


# ============================================================
# 5. Основная функция
# ============================================================
def main():
    """Главная функция: парсинг и загрузка в БД"""
    print("=" * 60)
    print("🚀 Graphite — Parser")
    print("=" * 60)

    # ---- Парсим файлы ----
    data = scan_obsidian_folder()
    print(f"\n📊 Всего обработано: {len(data)} файлов")

    if not data:
        print("❌ Нет данных для обработки")
        return

    # ---- Сохраняем JSON для отладки ----
    save_to_json(data)

    # ---- Показываем пример ----
    print("\n📄 Пример первой записи:")
    example = data[0]
    print(f"  Имя: {example['name']}")
    print(f"  Тип: {example['type']}")
    print(f"  Телефон: {example['phone']}")
    print(f"  Email: {example['email']}")
    print(f"  Telegram: {example['telegram']}")
    print(f"  Увлечения: {', '.join(example['hobbies'])}")
    print(f"  Организация: {example['organization']}")
    print(f"  Адрес: {example['address']}")
    print(f"  Связей: {len(example['connections'])}")
    print(f"  Wiki-ссылки: {len(example['wiki_links'])}")

    # ---- Загружаем в БД ----
    print("\n📤 Загрузка в базу данных...")

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(config.DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        load_to_database(data, session)
        print("\n✅ Данные успешно загружены в БД!")
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка при загрузке: {e}")
        raise
    finally:
        session.close()


# ============================================================
# Запуск
# ============================================================
if __name__ == '__main__':
    main()
