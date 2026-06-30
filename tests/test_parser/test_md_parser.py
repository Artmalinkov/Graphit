'''
Тесты для парсера
'''
# tests/test_md_parser.py
import pytest
from pathlib import Path
from src.parser.md_parser import parse_md_file


def test_parse_md_file_basic():
    # 1. Подготовка (Arrange)
    file_path = Path("tests/fixtures/sample_note.md")

    # 2. Действие (Act)
    result = parse_md_file(file_path)

    # 3. Проверка (Assert)
    assert result['name'] == "Иванов Иван Иванович"
    assert result['phone'] == "79787778899"
    assert result['email'] == "for_example@mail.ru"


def test_parse_md_file_basic():
    """Проверяет, что парсинг работает корректно"""
    result = parse_md_file(Path("tests/fixtures/ivanov.md"))

    assert result['name'] == "Иванов Иван Иванович"
    assert result['first_name'] == "Иван"
    assert result['last_name'] == "Иванов"
    assert result['phone'] == "79787778899"


def test_parse_md_file_no_phone():
    """Проверяет, что если телефона нет — возвращает None"""
    result = parse_md_file(Path("tests/fixtures/no_phone.md"))
    assert result['phone'] is None


def test_parse_md_file_with_hobbies():
    """Проверяет, что хобби парсятся корректно"""
    result = parse_md_file(Path("tests/fixtures/with_hobbies.md"))
    assert "футбол" in result['hobbies']
    assert "программирование" in result['hobbies']