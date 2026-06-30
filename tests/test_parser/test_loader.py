'''
Тесты для загрузчика
'''


def test_load_to_database(db_session):
    """Проверяет, что данные загружаются в БД"""
    data = [{
        'name': 'Тестовый Человек',
        'phone': '79990001122',
        'email': 'test@test.ru',
    }]

    load_to_database(data, db_session)

    person = db_session.query(Person).filter_by(name='Тестовый Человек').first()
    assert person is not None
    assert person.phone == '79990001122'