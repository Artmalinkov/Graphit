# src/models/addresses.py
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    full_address = Column(Text, nullable=False)
    country = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    street = Column(String(255), nullable=True)
    house = Column(String(20), nullable=True)
    apartment = Column(String(20), nullable=True)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "address", Connection.target_id == Address.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"