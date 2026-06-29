# src/models/connections.py
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey,
    JSON, DateTime, Index, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Connection(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True, index=True)

    source_type = Column(String(50), ForeignKey('entity_types.name', ondelete='RESTRICT'), nullable=False)
    source_id = Column(Integer, nullable=False)
    target_type = Column(String(50), ForeignKey('entity_types.name', ondelete='RESTRICT'), nullable=False)
    target_id = Column(Integer, nullable=False)

    relation_type = Column(String(50), nullable=False)

    strength = Column(Integer, default=3)
    description = Column(Text, nullable=True)
    attributes = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.now)

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

    # === Связи с EntityType ===
    source_type_ref = relationship('EntityType', foreign_keys=[source_type])
    target_type_ref = relationship('EntityType', foreign_keys=[target_type])

    # === Связи с Person ===
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

    # === Связи с Organization ===
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

    # === Связи с Address (только цель) ===
    target_address = relationship(
        'Address',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "address", Connection.target_id == Address.id)',
        viewonly=True
    )

    # === Связи с Industry (только цель) ===
    target_industry = relationship(
        'Industry',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "industry", Connection.target_id == Industry.id)',
        viewonly=True
    )

    # === Связи с Phone (только цель) ===
    target_phone = relationship(
        'Phone',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "phone", Connection.target_id == Phone.id)',
        viewonly=True
    )

    # === Связи с Email (только цель) ===
    target_email = relationship(
        'Email',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "email", Connection.target_id == Email.id)',
        viewonly=True
    )

    # === Связи с Hobby (только цель) ===
    target_hobby = relationship(
        'Hobby',
        foreign_keys=[target_id],
        primaryjoin='and_(Connection.target_type == "hobby", Connection.target_id == Hobby.id)',
        viewonly=True
    )

    def __repr__(self):
        return f"<Connection(id={self.id}, {self.source_type}:{self.source_id} -> {self.target_type}:{self.target_id}, type='{self.relation_type}')>"