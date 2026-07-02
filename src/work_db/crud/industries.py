# src/work_db/crud/industries.py
'''
CRUD-операции для таблицы industries
'''

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from src.models import Industry


def create_industry(session: Session, data: Dict[str, Any]) -> Industry:
    """Создаёт сферу деятельности"""
    industry = Industry(
        name=data.get('name'),
        description=data.get('description'),
        parent_id=data.get('parent_id')
    )
    session.add(industry)
    session.flush()
    return industry


def get_industry_by_id(session: Session, industry_id: int) -> Optional[Industry]:
    """Находит сферу по ID"""
    return session.query(Industry).filter_by(id=industry_id).first()


def get_industry_by_name(session: Session, name: str) -> Optional[Industry]:
    """Находит сферу по названию"""
    return session.query(Industry).filter_by(name=name).first()


def get_all_industries(session: Session) -> List[Industry]:
    """Возвращает все сферы деятельности"""
    return session.query(Industry).all()


def get_industries_by_parent(
        session: Session,
        parent_id: Optional[int] = None
) -> List[Industry]:
    """Возвращает сферы с указанным родителем"""
    return session.query(Industry).filter_by(parent_id=parent_id).all()


def get_root_industries(session: Session) -> List[Industry]:
    """Возвращает корневые сферы (без родителя)"""
    return get_industries_by_parent(session, None)


def update_industry(
        session: Session,
        industry_id: int,
        data: Dict[str, Any]
) -> Optional[Industry]:
    """Обновляет сферу деятельности"""
    industry = get_industry_by_id(session, industry_id)
    if not industry:
        return None

    updatable_fields = ['name', 'description', 'parent_id']
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(industry, field, data[field])

    session.flush()
    return industry


def delete_industry(session: Session, industry_id: int) -> bool:
    """Удаляет сферу деятельности"""
    industry = get_industry_by_id(session, industry_id)
    if not industry:
        return False
    session.delete(industry)
    session.flush()
    return True
