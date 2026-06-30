# src/models/telegrams.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Telegram(Base):
    __tablename__ = 'telegrams'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    type = Column(String(50), nullable=True)      # Тип: личный, рабочий
    is_primary = Column(Boolean, default=False) # Основной или нет
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "telegram", Connection.target_id == Telegram.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Telegram(id={self.id}, username='{self.username}')>"