from datetime import UTC, datetime

import pytest

from src.domain.entities.chat import Chat
from src.domain.entities.company import Company
from src.domain.entities.contact import Contact
from src.domain.entities.message import Message
from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.helpers.helpers import generate_uuid4


@pytest.fixture
def company_factory(company_repository):
    def _create_company(**kwargs):
        company_data = {
            "id": generate_uuid4(),
            "name": "Company Test",
        }
        company_data.update(**kwargs)
        company = Company(**company_data)
        company_repository.save(company)
        return company

    return _create_company


@pytest.fixture
def user_factory(company, user_repository):
    def _create_user(**kwargs):
        user_data = {
            "id": generate_uuid4(),
            "name": "Test User",
            "email": "email@gmail.com",
            "type": UserTypes.STAFF,
            "company_id": company.id,
        }
        user_data.update(**kwargs)
        user = User(**user_data)
        user_repository.save(user)
        return user

    return _create_user


@pytest.fixture
def contact_factory(company, contact_repository):
    def _create_contact(**kwargs):
        contact_data = {
            "id": generate_uuid4(),
            "name": "Contact Name",
            "phone_number": "5588999034444",
            "company_id": company.id,
            "created_at": None,
            "updated_at": None,
        }
        contact_data.update(**kwargs)
        contact = Contact(**contact_data)
        contact_repository.save(contact)
        return contact

    return _create_contact


@pytest.fixture
def chat_factory(company, sender_contact, chat_repository):
    def _create_chat(**kwargs):
        chat_data = {
            "id": generate_uuid4(),
            "company_id": company.id,
            "contact_id": sender_contact.id,
        }
        chat_data.update(**kwargs)
        chat = Chat(**chat_data)
        chat_repository.save(chat)
        return chat

    return _create_chat


@pytest.fixture
def message_factory(chat, receiver_contact, message_repository):
    def _create_message(**kwargs):
        message_data = {
            "id": generate_uuid4(),
            "external_id": "wamid.HBgLNTUxMTk4ODg4Nzc3NhUCABIYFDNFNkA1NkUwRjIyNUEzQTZEMTAA",
            "external_timestamp": datetime(2025, 11, 2, tzinfo=UTC),
            "chat_id": chat.id,
            "received_by": receiver_contact.id,
            "is_received": True,
            "text": "Text",
        }
        message_data.update(**kwargs)
        message = Message(**message_data)
        message_repository.save(message)
        return message

    return _create_message
