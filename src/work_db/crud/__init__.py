# src/work_db/crud/__init__.py
'''
CRUD-операции для работы с базой данных Graphite. Экспорт всех CRUD-функций
'''

from .entity_types import (
    get_or_create_entity_type,
    get_entity_type_by_name,
    get_all_entity_types,
)

from .persons import (
    create_person,
    get_person_by_id,
    get_person_by_full_name,
    get_person_by_name_parts,
    get_all_persons,
    search_persons,
    update_person,
    delete_person,
)

from .organizations import (
    create_organization,
    get_organization_by_id,
    get_organization_by_name,
    get_all_organizations,
    search_organizations,
    update_organization,
    delete_organization,
)

from .industries import (
    create_industry,
    get_industry_by_id,
    get_industry_by_name,
    get_all_industries,
    get_industries_by_parent,
    update_industry,
    delete_industry,
)

from .addresses import (
    create_address,
    get_address_by_id,
    get_address_by_full_address,
    get_all_addresses,
    search_addresses,
    update_address,
    delete_address,
)

from .phones import (
    create_phone,
    get_phone_by_id,
    get_phone_by_number,
    get_all_phones,
    update_phone,
    delete_phone,
)

from .emails import (
    create_email,
    get_email_by_id,
    get_email_by_address,
    get_all_emails,
    update_email,
    delete_email,
)

from .telegrams import (
    create_telegram,
    get_telegram_by_id,
    get_telegram_by_username,
    get_all_telegrams,
    update_telegram,
    delete_telegram,
)

from .hobbies import (
    create_hobby,
    get_hobby_by_id,
    get_hobby_by_name,
    get_all_hobbies,
    search_hobbies,
    update_hobby,
    delete_hobby,
)

from .connections import (
    create_connection,
    get_connection_by_id,
    get_connections_for_entity,
    get_connections_between,
    get_outgoing_connections,
    get_incoming_connections,
    update_connection,
    delete_connection,
    delete_connections_for_entity,
)

__all__ = [
    # Entity Types
    'get_or_create_entity_type',
    'get_entity_type_by_name',
    'get_all_entity_types',

    # Persons
    'create_person',
    'get_person_by_id',
    'get_person_by_full_name',
    'get_person_by_name_parts',
    'get_all_persons',
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
    'create_connection',
    'get_connection_by_id',
    'get_connections_for_entity',
    'get_connections_between',
    'get_outgoing_connections',
    'get_incoming_connections',
    'update_connection',
    'delete_connection',
    'delete_connections_for_entity',
]