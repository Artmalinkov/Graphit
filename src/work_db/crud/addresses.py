# src/work_db/crud/addresses.py
'''
CRUD-операции для таблицы addresses
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Address


def create_address(session: Session, data: Dict[str, Any]) -> Address:
    """Создаёт адрес"""
    address = Address(
        full_address=data.get('full_address'),
        country=data.get('country'),
        region=data.get('region'),
        city=data.get('city'),
        street=data.get('street'),
        house=data.get('house'),
        apartment=data.get('apartment'),
        postal_code=data.get('postal_code'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        notes=data.get('notes')
    )
    session.add(address)
    session.flush()
    return address


def get_address_by_id(session: Session, address_id: int) -> Optional[Address]:
    """Находит адрес по ID"""
    return session.query(Address).filter_by(id=address_id).first()


def get_address_by_full_address(session: Session, full_address: str) -> Optional[Address]:
    """Находит адрес по полному адресу"""
    return session.query(Address).filter_by(full_address=full_address).first()


def get_all_addresses(session: Session) -> List[Address]:
    """Возвращает все адреса"""
    return session.query(Address).all()


def search_addresses(session: Session, query: str) -> List[Address]:
    """Ищет адреса по городу или улице"""
    search_pattern = f"%{query}%"
    return session.query(Address).filter(
        or_(
            Address.full_address.ilike(search_pattern),
            Address.city.ilike(search_pattern),
            Address.street.ilike(search_pattern),
        )
    ).all()


def update_address(session: Session, address_id: int, data: Dict[str, Any]) -> Optional[Address]:
    """Обновляет адрес"""
    address = get_address_by_id(session, address_id)
    if not address:
        return None

    updatable_fields = [
        'full_address', 'country', 'region', 'city', 'street',
        'house', 'apartment', 'postal_code', 'latitude', 'longitude', 'notes'
    ]
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(address, field, data[field])

    session.flush()
    return address


def delete_address(session: Session, address_id: int) -> bool:
    """Удаляет адрес"""
    address = get_address_by_id(session, address_id)
    if not address:
        return False
    session.delete(address)
    session.flush()
    return True