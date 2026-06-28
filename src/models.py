# src/models.py
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey,
    JSON, DECIMAL, TIMESTAMP, Boolean,
    UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# ============================================================
# 1. Справочник типов сущностей
# ============================================================
class EntityType(Base):
    __tablename__ = 'entity_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    # Связи (для удобства)
    source_connections = relationship(
        'Connection',
        foreign_keys='Connection.source_type',
        primaryjoin='EntityType.name == Connection.source_type',
        viewonly=True
    )
    target_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_type',
        primaryjoin='EntityType.name == Connection.target_type',
        viewonly=True
    )

    def __repr__(self):
        return f"<EntityType(name='{self.name}')>"


# ============================================================
# 2. Физические лица
# ============================================================
class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    birth_date = Column(TIMESTAMP, nullable=True)
    telegram = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    hobbies = Column(JSON, nullable=True)  # Храним как JSON массив
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    # Связи (как источник)
    outgoing_connections = relationship(
        'Connection',
        foreign_keys='Connection.source_id',
        primaryjoin='and_(Connection.source_type == "person", Connection.source_id == Person.id)',
        back_populates='source_person'
    )
    # Связи (как цель)
    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "person", Connection.target_id == Person.id)',
        back_populates='target_person'
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"


# ============================================================
# 3. Организации
# ============================================================
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
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    # Связи (как источник)
    outgoing_connections = relationship(
        'Connection',
        foreign_keys='Connection.source_id',
        primaryjoin='and_(Connection.source_type == "organization", Connection.source_id == Organization.id)',
        back_populates='source_organization'
    )
    # Связи (как цель)
    incoming_connections = relationship(
        'Connection',
        foreign_keys='Connection.target_id',
        primaryjoin='and_(Connection.target_type == "organization", Connection.target_id == Organization.id)',
        back_populates='target_organization'
    )

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"


# ============================================================
# 4. Сферы деятельности
# ============================================================
class Industry(Base):
    __tablename__ = 'industries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey('industries.id'), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    # Иерархия
    children = relationship('Industry', backref='parent', remote_side=[id])

    def __repr__(self):
        return f"<Industry(id={self.id}, name='{self.name}')>"


# ============================================================
# 5. Адреса
# ============================================================
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
    latitude = Column(DECIMAL(10, 8), nullable=True)
    longitude = Column(DECIMAL(11, 8), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}')>"


# ============================================================
# 6. Связи (универсальная таблица)
# ============================================================
class Connection(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True, index=True)

    # Типы сущностей (ссылаются на entity_types.name)
    source_type = Column(String(50), ForeignKey('entity_types.name', ondelete='RESTRICT'), nullable=False)
    source_id = Column(Integer, nullable=False)
    target_type = Column(String(50), ForeignKey('entity_types.name', ondelete='RESTRICT'), nullable=False)
    target_id = Column(Integer, nullable=False)

    # Тип связи (свободная строка, но можно тоже сделать справочником)
    relation_type = Column(String(50), nullable=False)

    # Атрибуты связи
    strength = Column(Integer, default=3)
    description = Column(Text, nullable=True)
    attributes = Column(JSON, nullable=True)  # Храним дополнительные данные (должность, даты и т.д.)

    created_at = Column(TIMESTAMP, default=datetime.now)

    # Индексы для производительности
    __table_args__ = (
        Index('idx_connections_source', 'source_type', 'source_id'),
        Index('idx_connections_target', 'target_type', 'target_id'),
        Index('idx_connections_relation', 'relation_type'),
        UniqueConstraint(
            'source_type', 'source_id',
            'target_type', 'target_id',
            'relation_type',
            name='uq_connection_unique'
        ),
    )

    # Связи для типов (справочник)
    source_type_ref = relationship('EntityType', foreign_keys=[source_type])
    target_type_ref = relationship('EntityType', foreign_keys=[target_type])

    # Связи для удобства (Person)
    source_person = relationship(
        'Person',
        foreign_keys=[source_id],
        primaryjoin='and_(Connection.source_type == "person", Connection.source_id == Person.id)',
        back_populates='outgoing_connections'
    )
    target_person = relationship(
        'Person',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "person", Connection.target_id == Person.id)',
        back_populates='incoming_connections'
    )

    # Связи для удобства (Organization)
    source_organization = relationship(
        'Organization',
        foreign_keys=[source_id],
        primaryjoin='and_(Connection.source_type == "organization", Connection.source_id == Organization.id)',
        back_populates='outgoing_connections'
    )
    target_organization = relationship(
        'Organization',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "organization", Connection.target_id == Organization.id)',
        back_populates='incoming_connections'
    )

    # Связи для Address и Industry (только как цель)
    target_address = relationship(
        'Address',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "address", Connection.target_id == Address.id)',
        viewonly=True
    )
    target_industry = relationship(
        'Industry',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "industry", Connection.target_id == Industry.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Connection(id={self.id}, {self.source_type}:{self.source_id} -> {self.target_type}:{self.target_id}, type='{self.relation_type}')>"