# src/models/industries.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Industry(Base):
    __tablename__ = 'industries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey('industries.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    children = relationship('Industry', backref='parent', remote_side=[id])

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "industry", Connection.target_id == Industry.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Industry(id={self.id}, name='{self.name}')>"