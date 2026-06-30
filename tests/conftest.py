# tests/conftest.py
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

@pytest.fixture
def db_session():
    """Временная БД в памяти для тестов"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_md_file():
    """Путь к тестовому .md файлу"""
    return Path(__file__).parent / "fixtures" / "sample.md"