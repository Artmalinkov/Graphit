# src/work_db/crud/organizations.py
'''
CRUD-операции для таблицы organizations
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Organization


def create_organization(session: Session, data: Dict[str, Any]) -> Organization:
    """Создаёт организацию"""
    organization = Organization(
        name=data.get('name'),
        full_name=data.get('full_name'),
        inn=data.get('inn'),
        ogrn=data.get('ogrn'),
        website=data.get('website'),
        industry=data.get('industry'),
        description=data.get('description'),
        notes=data.get('notes')
    )
    session.add(organization)
    session.flush()
    return organization


def get_organization_by_id(session: Session, org_id: int) -> Optional[Organization]:
    """Находит организацию по ID"""
    return session.query(Organization).filter_by(id=org_id).first()


def get_organization_by_name(session: Session, name: str) -> Optional[Organization]:
    """Находит организацию по названию"""
    return session.query(Organization).filter_by(name=name).first()


def get_all_organizations(session: Session) -> List[Organization]:
    """Возвращает все организации"""
    return session.query(Organization).all()


def search_organizations(session: Session, query: str) -> List[Organization]:
    """Ищет организации по названию или ИНН"""
    search_pattern = f"%{query}%"
    return session.query(Organization).filter(
        or_(
            Organization.name.ilike(search_pattern),
            Organization.full_name.ilike(search_pattern),
            Organization.inn.ilike(search_pattern),
        )
    ).all()


def update_organization(session: Session, org_id: int, data: Dict[str, Any]) -> Optional[Organization]:
    """Обновляет данные организации"""
    organization = get_organization_by_id(session, org_id)
    if not organization:
        return None

    updatable_fields = ['name', 'full_name', 'inn', 'ogrn', 'website', 'industry', 'description', 'notes']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(organization, field, data[field])

    session.flush()
    return organization


def delete_organization(session: Session, org_id: int) -> bool:
    """Удаляет организацию"""
    organization = get_organization_by_id(session, org_id)
    if not organization:
        return False
    session.delete(organization)
    session.flush()
    return True
