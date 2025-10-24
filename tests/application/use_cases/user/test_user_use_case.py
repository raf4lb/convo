import pytest

from src.application.exceptions import UserNotFoundError
from src.application.use_cases.user.user_use_cases import (
    CreateUserUseCase,
    UpdateUserUseCase,
)


def test_create_user_use_case(staff_user, user_repository):
    # Arrange
    create_use_case = CreateUserUseCase(repository=user_repository)
    # Act
    create_use_case.execute(staff_user)
    # Assert
    assert staff_user.id in {user.id for user in user_repository.get_users()}


def test_update_user_use_case_existing_user(staff_user, user_repository):
    # Arrange
    user_repository.create_user(staff_user)
    update_use_case = UpdateUserUseCase(repository=user_repository)

    # Act
    new_name = "New Name"
    staff_user.name = new_name
    update_use_case.execute(staff_user)

    # Assert
    user = user_repository.get_user_by_id(staff_user.id)
    assert user.name == new_name


def test_update_user_use_case_non_existing_user(staff_user, user_repository):
    # Arrange
    update_use_case = UpdateUserUseCase(repository=user_repository)
    # Act/Assert
    with pytest.raises(UserNotFoundError):
        update_use_case.execute(staff_user)
