import uuid

import pytest

from src.application.use_cases.message.message_use_cases import DeleteMessageUseCase
from src.application.use_cases.user.user_use_cases import (
    CreateUserUseCase,
    UpdateUserUseCase,
)
from src.domain.enums import UserTypes
from src.domain.errors import UserNotFoundError


def test_create_user_use_case(user_repository):
    # Arrange
    name = "Test User"
    email = "email@test.com"
    type = UserTypes.STAFF
    use_case = CreateUserUseCase(repository=user_repository)

    # Act
    user = use_case.execute(
        name=name,
        email=email,
        type=type,
        company_id=str(uuid.uuid4()),
    )

    # Assert
    assert user_repository.get_by_id(user.id) is not None


def test_update_user_use_case_existing_user(staff_user, user_repository):
    # Arrange
    user_repository.save(staff_user)
    use_case = UpdateUserUseCase(repository=user_repository)

    # Act
    new_name = "New Name"
    use_case.execute(
        user_id=staff_user.id,
        name=new_name,
        email=staff_user.email,
        type=staff_user.type,
        company_id=str(uuid.uuid4()),
    )

    # Assert
    user = user_repository.get_by_id(staff_user.id)
    assert user.name == new_name


def test_update_user_use_case_non_existing_user(staff_user, user_repository):
    # Arrange
    use_case = UpdateUserUseCase(repository=user_repository)

    # Act/Assert
    with pytest.raises(UserNotFoundError):
        use_case.execute(
            user_id=staff_user.id,
            name="New Name",
            email=staff_user.email,
            type=staff_user.type,
            company_id=str(uuid.uuid4()),
        )


def test_delete_user_use_case(staff_user, user_repository):
    # Arrange
    user_repository.save(staff_user)
    use_case = DeleteMessageUseCase(repository=user_repository)

    # Act
    use_case.execute(staff_user.id)

    # Act/Assert
    with pytest.raises(UserNotFoundError):
        user_repository.get_by_id(staff_user.id)
