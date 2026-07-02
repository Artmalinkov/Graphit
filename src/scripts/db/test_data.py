# src/scripts/db/test_data.py
"""
Тестовые данные для заполнения базы
"""

from datetime import datetime, timedelta
import random


# ============================================================
# ЛЮДИ
# ============================================================

PEOPLE = [
    {
        "full_name": "Иванов Иван Иванович",
        "name": "Иван",
        "family_name": "Иванов",
        "father_name": "Иванович",
        "birth_date": datetime(1990, 1, 15),
        "notes": "Любит футбол и программирование"
    },
    {
        "full_name": "Петров Петр Петрович",
        "name": "Петр",
        "family_name": "Петров",
        "father_name": "Петрович",
        "birth_date": datetime(1985, 5, 20),
        "notes": "Работает в IT, увлекается фотографией"
    },
    {
        "full_name": "Сидорова Анна Сергеевна",
        "name": "Анна",
        "family_name": "Сидорова",
        "father_name": "Сергеевна",
        "birth_date": datetime(1992, 8, 10),
        "notes": "Дизайнер, любит рисовать"
    },
    {
        "full_name": "Козлов Дмитрий Алексеевич",
        "name": "Дмитрий",
        "family_name": "Козлов",
        "father_name": "Алексеевич",
        "birth_date": datetime(1988, 11, 3),
        "notes": "Предприниматель, владелец бизнеса"
    },
    {
        "full_name": "Морозова Екатерина Владимировна",
        "name": "Екатерина",
        "family_name": "Морозова",
        "father_name": "Владимировна",
        "birth_date": datetime(1995, 3, 25),
        "notes": "Маркетолог, увлекается SMM"
    },
    {
        "full_name": "Соколов Алексей Андреевич",
        "name": "Алексей",
        "family_name": "Соколов",
        "father_name": "Андреевич",
        "birth_date": datetime(1991, 7, 12),
        "notes": "Разработчик, любит футбол"
    },
    {
        "full_name": "Николаева Ольга Павловна",
        "name": "Ольга",
        "family_name": "Николаева",
        "father_name": "Павловна",
        "birth_date": datetime(1989, 9, 8),
        "notes": "Менеджер, увлекается плаванием"
    },
    {
        "full_name": "Федоров Игорь Николаевич",
        "name": "Игорь",
        "family_name": "Федоров",
        "father_name": "Николаевич",
        "birth_date": datetime(1986, 12, 1),
        "notes": "Директор по развитию"
    },
    {
        "full_name": "Волкова Мария Александровна",
        "name": "Мария",
        "family_name": "Волкова",
        "father_name": "Александровна",
        "birth_date": datetime(1993, 6, 17),
        "notes": "HR-специалист"
    },
    {
        "full_name": "Зайцев Константин Владимирович",
        "name": "Константин",
        "family_name": "Зайцев",
        "father_name": "Владимирович",
        "birth_date": datetime(1987, 2, 28),
        "notes": "Финансовый аналитик"
    },
]


# ============================================================
# ОРГАНИЗАЦИИ
# ============================================================

ORGANIZATIONS = [
    {
        "name": "Яндекс",
        "full_name": "ООО «Яндекс»",
        "inn": "7736207543",
        "website": "https://yandex.ru",
        "industry": "IT",
        "description": "Поисковая система и IT-компания"
    },
    {
        "name": "Сбербанк",
        "full_name": "ПАО «Сбербанк»",
        "inn": "7707083893",
        "website": "https://sberbank.ru",
        "industry": "Финансы",
        "description": "Крупнейший банк России"
    },
    {
        "name": "Дизайн-студия «Арт»",
        "full_name": "ООО «Арт-Дизайн»",
        "inn": "1234567890",
        "website": "https://art-design.ru",
        "industry": "Дизайн",
        "description": "Студия веб-дизайна"
    },
    {
        "name": "IT-Решения",
        "full_name": "ООО «IT-Решения»",
        "inn": "9876543210",
        "website": "https://it-solutions.ru",
        "industry": "IT",
        "description": "Разработка ПО и консалтинг"
    },
    {
        "name": "Медиа-Группа",
        "full_name": "ООО «Медиа-Группа»",
        "inn": "1122334455",
        "website": "https://media-group.ru",
        "industry": "Маркетинг",
        "description": "Маркетинговое агентство"
    },
    {
        "name": "ТехноСтрой",
        "full_name": "ООО «ТехноСтрой»",
        "inn": "5566778899",
        "website": "https://tehnostroy.ru",
        "industry": "Строительство",
        "description": "Строительная компания"
    },
]


# ============================================================
# СФЕРЫ ДЕЯТЕЛЬНОСТИ
# ============================================================

INDUSTRIES = [
    {"name": "IT", "description": "Информационные технологии"},
    {"name": "Финансы", "description": "Банки, инвестиции, страхование"},
    {"name": "Дизайн", "description": "Веб-дизайн, графический дизайн, UX/UI"},
    {"name": "Программирование", "description": "Разработка ПО"},
    {"name": "Маркетинг", "description": "Цифровой маркетинг, SMM"},
    {"name": "Банковское дело", "description": "Банковские услуги"},
    {"name": "Медицина", "description": "Здравоохранение, медицина"},
    {"name": "Образование", "description": "Обучение, курсы, университеты"},
    {"name": "Строительство", "description": "Строительство и архитектура"},
]


# ============================================================
# ТЕЛЕФОНЫ
# ============================================================

PHONES = [
    {"number": "+7 999 123-45-67", "type": "mobile", "is_primary": True},
    {"number": "+7 999 987-65-43", "type": "mobile", "is_primary": True},
    {"number": "+7 999 555-55-55", "type": "work", "is_primary": False},
    {"number": "+7 999 111-22-33", "type": "mobile", "is_primary": True},
    {"number": "+7 999 444-55-66", "type": "work", "is_primary": False},
    {"number": "+7 999 777-88-99", "type": "mobile", "is_primary": True},
    {"number": "+7 999 222-33-44", "type": "mobile", "is_primary": True},
    {"number": "+7 999 888-99-00", "type": "work", "is_primary": False},
]


# ============================================================
# EMAIL
# ============================================================

EMAILS = [
    {"address": "ivanov@mail.ru", "type": "personal", "is_primary": True},
    {"address": "petrov@yandex.ru", "type": "personal", "is_primary": True},
    {"address": "petrov@yandex-team.ru", "type": "work", "is_primary": False},
    {"address": "sidorova@design.ru", "type": "personal", "is_primary": True},
    {"address": "kozlov@business.ru", "type": "personal", "is_primary": True},
    {"address": "morozova@marketing.ru", "type": "personal", "is_primary": True},
    {"address": "sokolov@it-solutions.ru", "type": "work", "is_primary": True},
    {"address": "nikolaeva@mg.ru", "type": "personal", "is_primary": True},
    {"address": "fedorov@tehno.ru", "type": "work", "is_primary": True},
]


# ============================================================
# TELEGRAM
# ============================================================

TELEGRAMS = [
    {"username": "@ivanov_i", "type": "personal", "is_primary": True},
    {"username": "@petrov_p", "type": "personal", "is_primary": True},
    {"username": "@petrov_work", "type": "work", "is_primary": False},
    {"username": "@sidorova_a", "type": "personal", "is_primary": True},
    {"username": "@kozlov_d", "type": "personal", "is_primary": True},
    {"username": "@morozova_e", "type": "personal", "is_primary": True},
    {"username": "@sokolov_a", "type": "work", "is_primary": True},
    {"username": "@nikolaeva_o", "type": "personal", "is_primary": True},
    {"username": "@fedorov_i", "type": "work", "is_primary": True},
]


# ============================================================
# ХОББИ
# ============================================================

HOBBIES = [
    {"name": "Футбол", "category": "sport", "description": "Играет в футбол по выходным"},
    {"name": "Программирование", "category": "tech", "description": "Пишет код на Python"},
    {"name": "Дизайн", "category": "art", "description": "Занимается веб-дизайном"},
    {"name": "Рисование", "category": "art", "description": "Рисует акварелью"},
    {"name": "Плавание", "category": "sport", "description": "Ходит в бассейн"},
    {"name": "Фотография", "category": "art", "description": "Снимает на зеркалку"},
    {"name": "Чтение", "category": "knowledge", "description": "Любит читать книги"},
    {"name": "Путешествия", "category": "life", "description": "Путешествует по миру"},
    {"name": "Йога", "category": "sport", "description": "Занимается йогой"},
    {"name": "Готовка", "category": "life", "description": "Любит готовить"},
    {"name": "Шахматы", "category": "knowledge", "description": "Играет в шахматы"},
    {"name": "Бег", "category": "sport", "description": "Бегает по утрам"},
]


# ============================================================
# СВЯЗИ МЕЖДУ ЛЮДЬМИ
# ============================================================

def get_connection_data():
    """
    Возвращает данные для связей между людьми
    """
    return [
        # (имя_источника, имя_цели, тип_связи, сила)
        ("Иванов Иван Иванович", "Петров Петр Петрович", "friend", 5),
        ("Иванов Иван Иванович", "Сидорова Анна Сергеевна", "colleague", 3),
        ("Иванов Иван Иванович", "Соколов Алексей Андреевич", "friend", 4),
        ("Петров Петр Петрович", "Козлов Дмитрий Алексеевич", "colleague", 4),
        ("Петров Петр Петрович", "Морозова Екатерина Владимировна", "acquaintance", 2),
        ("Петров Петр Петрович", "Соколов Алексей Андреевич", "colleague", 4),
        ("Сидорова Анна Сергеевна", "Морозова Екатерина Владимировна", "friend", 4),
        ("Сидорова Анна Сергеевна", "Николаева Ольга Павловна", "friend", 3),
        ("Козлов Дмитрий Алексеевич", "Федоров Игорь Николаевич", "colleague", 5),
        ("Козлов Дмитрий Алексеевич", "Зайцев Константин Владимирович", "friend", 3),
        ("Морозова Екатерина Владимировна", "Волкова Мария Александровна", "friend", 4),
        ("Соколов Алексей Андреевич", "Николаева Ольга Павловна", "colleague", 3),
        ("Николаева Ольга Павловна", "Волкова Мария Александровна", "friend", 3),
        ("Федоров Игорь Николаевич", "Зайцев Константин Владимирович", "colleague", 4),
        ("Волкова Мария Александровна", "Зайцев Константин Владимирович", "acquaintance", 2),
    ]