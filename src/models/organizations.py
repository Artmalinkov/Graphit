# src/models/organizations.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    full_name = Column(String(500), nullable=True)
    inn = Column(String(20), nullable=True)
    ogrn = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    outgoing_connections = relationship(
        'Connection',
        foreign_keys='Connection.source_id',
        primaryjoin='and_(Connection.source_type == "organization", Connection.source_id == Organization.id)',
        back_populates='source_organization',
        cascade='all, delete-orphan'
    )

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "organization", Connection.target_id == Organization.id)',
        back_populates='target_organization',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"