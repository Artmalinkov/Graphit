# src/models/phones.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False, unique=True)
    type = Column(String(50), nullable=True)      # mobile, work, home, fax
    is_primary = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "phone", Connection.target_id == Phone.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Phone(id={self.id}, number='{self.number}')>"