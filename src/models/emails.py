# src/models/emails.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=True)      # personal, work, other
    is_primary = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "email", Connection.target_id == Email.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Email(id={self.id}, address='{self.address}')>"