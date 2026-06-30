'''
Интеграционные тесты
'''


def test_full_pipeline(db_session):
    """Проверяет полный процесс: парсинг → загрузка"""
    data = scan_obsidian_folder()
    load_to_database(data, db_session)

    count = db_session.query(Person).count()
    assert count > 0