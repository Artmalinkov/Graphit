# src/models/persons.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    birth_date = Column(DateTime, nullable=True)
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