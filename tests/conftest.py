import uuid

import pytest

from src.domain.entities.company import Company
from src.domain.entities.user import User
from src.domain.enums import UserTypes
from src.infrastructure.repositories.company_repository import InMemoryCompanyRepository
from src.infrastructure.repositories.user_repository import InMemoryUserRepository


@pytest.fixture
def staff_user():
    return User(
        id=uuid.uuid4(),
        name="Test User",
        email="email@gmail.com",
        type=UserTypes.STAFF,
    )


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def company():
    return Company(
        id=uuid.uuid4(),
        name="Company Name",
    )

@pytest.fixture
def company_repository():
    return InMemoryCompanyRepository()
