'''
Тесты для CRUD-операций
'''


def test_create_person(db_session):
    """Проверяет создание человека"""
    person = create_person(db_session, {'name': 'Тест', 'first_name': 'Тестович'})

    assert person.id is not None
    assert person.name == 'Тест'


def test_get_person_by_name(db_session):
    """Проверяет поиск человека по имени"""
    create_person(db_session, {'name': 'Иван Петров'})

    person = get_person_by_name(db_session, 'Иван Петров')
    assert person is not None
    assert person.name == 'Иван Петров'