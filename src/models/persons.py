# src/models/persons.py
'''
Модуль для опеределении таблицы persons в БД
'''
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from datetime import datetime
import enum


from .base import Base

class Gender(str, enum.Enum):
    """Перечисление возможных значений пола"""
    MALE = 'male'
    FEMALE = 'female'

class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    family_name = Column(String(100), nullable=True)
    name = Column(String(100), nullable=True)
    father_name = Column(String(100), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    gender = Column(SAEnum(Gender), nullable=True, default=None)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Исходящие связи (человек → кто-то/что-то)
    outgoing_connections = relationship(
        'Connection',
        foreign_keys='Connection.source_id',
        primaryjoin='and_(Connection.source_type == "person", Connection.source_id == Person.id)',
        back_populates='source_person',
        cascade='all, delete-orphan'
    )

    # Входящие связи (кто-то/что-то → человек)
    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "person", Connection.target_id == Person.id)',
        back_populates='target_person',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"