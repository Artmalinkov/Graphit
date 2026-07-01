# src/work_db/crud/base.py
'''
Базовые CRUD-функции для всех моделей
'''

from typing import Optional, TypeVar, Generic, Type, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseCRUD(Generic[ModelType]):
    """
    Базовый класс для CRUD-операций
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, session: Session, **kwargs) -> ModelType:
        """Создаёт новую запись"""
        instance = self.model(**kwargs)
        session.add(instance)
        session.flush()
        return instance

    def get_by_id(self, session: Session, id: int) -> Optional[ModelType]:
        """Находит запись по ID"""
        return session.query(self.model).filter_by(id=id).first()

    def get_all(self, session: Session) -> List[ModelType]:
        """Возвращает все записи"""
        return session.query(self.model).all()

    def update(self, session: Session, id: int, **kwargs) -> Optional[ModelType]:
        """Обновляет запись"""
        instance = self.get_by_id(session, id)
        if not instance:
            return None
        for key, value in kwargs.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        session.flush()
        return instance

    def delete(self, session: Session, id: int) -> bool:
        """Удаляет запись"""
        instance = self.get_by_id(session, id)
        if not instance:
            return False
        session.delete(instance)
        session.flush()
        return True
