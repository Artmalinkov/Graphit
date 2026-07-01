-- Очищаем таблицу (если есть данные)
DELETE FROM entity_types;

-- Вставляем базовые типы
INSERT INTO entity_types (name, description, is_active) VALUES
    ('person', 'Физическое лицо (человек)', 1),
    ('organization', 'Юридическое лицо (компания, организация)', 1),
    ('address', 'Адрес (географическая точка)', 1),
    ('industry', 'Сфера деятельности', 1),
    ('phone', 'Телефонный номер', 1),
    ('email', 'Электронная почта', 1),
    ('telegram', 'Telegram-аккаунт', 1),
    ('hobby', 'Хобби / увлечение', 1);

-- Проверяем
SELECT * FROM entity_types;