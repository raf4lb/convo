import pytest

from tests.fakes.repositories.in_memory_chat_repository import (
    InMemoryChatRepository,
)
from tests.fakes.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from tests.fakes.repositories.in_memory_contact_repository import (
    InMemoryContactRepository,
)
from tests.fakes.repositories.in_memory_message_repository import (
    InMemoryMessageRepository,
)
from tests.fakes.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


@pytest.fixture
def company_repository():
    return InMemoryCompanyRepository()


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def contact_repository():
    return InMemoryContactRepository()


@pytest.fixture
def chat_repository():
    return InMemoryChatRepository()


@pytest.fixture
def message_repository():
    return InMemoryMessageRepository()
