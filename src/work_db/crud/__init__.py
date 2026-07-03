# src/work_db/crud/__init__.py
'''
CRUD-операции для работы с базой данных Graphite. Экспорт всех CRUD-функций
'''

from .entity_types import *
from .persons import *
from .organizations import *
from .industries import *
from .addresses import *
from .phones import *
from .emails import *
from .telegrams import *
from .hobbies import *
from .connections import *

__all__ = (
    # Entity Types
    'get_or_create_entity_type',
    'get_entity_type_by_name',
    'get_all_entity_types',
    'update_entity_type',
    'delete_entity_type',

    # Persons
    'create_person',
    'get_person_by_id',
    'get_person_by_full_name',
    'get_person_by_name_parts',
    'get_all_persons',
    'get_persons_by_gender',
    'get_persons_with_gender',
    'get_persons_without_gender',
    'search_persons',
    'update_person',
    'delete_person',

    # Organizations
    'create_organization',
    'get_organization_by_id',
    'get_organization_by_name',
    'get_all_organizations',
    'search_organizations',
    'update_organization',
    'delete_organization',

    # Industries
    'create_industry',
    'get_industry_by_id',
    'get_industry_by_name',
    'get_all_industries',
    'get_industries_by_parent',
    'update_industry',
    'delete_industry',

    # Addresses
    'create_address',
    'get_address_by_id',
    'get_address_by_full_address',
    'get_all_addresses',
    'search_addresses',
    'update_address',
    'delete_address',

    # Phones
    'create_phone',
    'get_phone_by_id',
    'get_phone_by_number',
    'get_all_phones',
    'update_phone',
    'delete_phone',

    # Emails
    'create_email',
    'get_email_by_id',
    'get_email_by_address',
    'get_all_emails',
    'update_email',
    'delete_email',

    # Telegrams
    'create_telegram',
    'get_telegram_by_id',
    'get_telegram_by_username',
    'get_all_telegrams',
    'update_telegram',
    'delete_telegram',

    # Hobbies
    'create_hobby',
    'get_hobby_by_id',
    'get_hobby_by_name',
    'get_all_hobbies',
    'search_hobbies',
    'update_hobby',
    'delete_hobby',

    # Connections
    'get_all_connections',
    'create_connection',
    'get_connection_by_id',
    'get_connections_for_entity',
    'get_connections_between',
    'get_outgoing_connections',
    'get_incoming_connections',
    'update_connection',
    'delete_connection',
    'delete_connections_for_entity',
)