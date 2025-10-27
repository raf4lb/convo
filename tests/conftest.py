import uuid

import pytest

from src.domain.entities.company import Company
from src.domain.entities.contact import Contact
from src.domain.entities.message import Message
from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.helpers.helpes import get_now_iso_format
from src.infrastructure.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from src.infrastructure.repositories.in_memory_contact_repository import (
    InMemoryContactRepository,
)
from src.infrastructure.repositories.in_memory_message_repository import (
    InMemoryMessageRepository,
)
from src.infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


@pytest.fixture
def company():
    created_at = get_now_iso_format()
    return Company(
        id=str(uuid.uuid4()),
        name="Company Name",
        created_at=created_at,
        updated_at=created_at,
    )


@pytest.fixture
def company_repository():
    return InMemoryCompanyRepository()


@pytest.fixture
def staff_user(company):
    created_at = get_now_iso_format()
    return User(
        id=str(uuid.uuid4()),
        name="Test User",
        email="email@gmail.com",
        type=UserTypes.STAFF,
        company_id=company.id,
        created_at=created_at,
        updated_at=created_at,
    )


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def message(company):
    created_at = get_now_iso_format()
    return Message(
        id=str(uuid.uuid4()),
        company_id=company.id,
        sender_id=str(uuid.uuid4()),
        receiver_id=str(uuid.uuid4()),
        received=True,
        text="Text",
        created_at=created_at,
        updated_at=created_at,
    )


@pytest.fixture
def message_repository():
    return InMemoryMessageRepository()


@pytest.fixture
def contact(company):
    created_at = get_now_iso_format()
    return Contact(
        id=str(uuid.uuid4()),
        name="Contact Name",
        phone_number="+5588999034444",
        company_id=company.id,
        created_at=created_at,
        updated_at=created_at,
    )


@pytest.fixture
def receiver_contact(contact):
    return contact


@pytest.fixture
def sender_contact(contact):
    contact.id = str(uuid.uuid4())
    contact.name = "Sender Contact"
    contact.phone_number = "+5588999034445"
    return contact


@pytest.fixture
def contact_repository():
    return InMemoryContactRepository()
