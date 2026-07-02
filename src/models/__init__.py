# src/models/__init__.py
from .base import Base
from .entity_types import EntityType
from .persons import Person, Gender
from .organizations import Organization
from .industries import Industry
from .addresses import Address
from .phones import Phone
from .telegrams import Telegram
from .emails import Email
from .hobbies import Hobby
from .connections import Connection

__all__ = [
    'Base',
    'EntityType',
    'Person',
    'Gender',
    'Organization',
    'Industry',
    'Address',
    'Phone',
    'Telegram',
    'Email',
    'Hobby',
    'Connection',
]