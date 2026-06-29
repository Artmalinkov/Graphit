# src/models/hobbies.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Hobby(Base):
    __tablename__ = 'hobbies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100), nullable=True)  # sport, art, science, etc.
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "hobby", Connection.target_id == Hobby.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Hobby(id={self.id}, name='{self.name}')>"