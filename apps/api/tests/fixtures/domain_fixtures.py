import pytest

from src.domain.enums import UserTypes


@pytest.fixture
def company(company_factory):
    return company_factory()


@pytest.fixture
def staff_user(user_factory):
    return user_factory(type=UserTypes.STAFF)


@pytest.fixture
def contact(contact_factory):
    return contact_factory()


@pytest.fixture
def receiver_contact(contact_factory):
    return contact_factory(
        name="Receiver Name",
        phone_number="5588999034444",
    )


@pytest.fixture
def sender_contact(contact_factory):
    return contact_factory(
        name="Sender Name",
        phone_number="5588999034445",
    )


@pytest.fixture
def chat(chat_factory):
    return chat_factory()


@pytest.fixture
def message(message_factory):
    return message_factory()
