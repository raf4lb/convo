import pytest

from src.application.exceptions import UserNotFoundError


def test_create_user(staff_user, user_repository):
    # Act
    user_repository.create_user(staff_user)
    # Assert
    assert staff_user.id in {user.id for user in user_repository.get_users()}


def test_updating_existing_user(staff_user, user_repository):
    # Arrange
    user_repository.create_user(staff_user)
    # Act
    new_name = "new name"
    staff_user.name = new_name
    user_repository.update_user(staff_user)
    # Assert
    user = user_repository.get_user_by_id(staff_user.id)
    assert user.name == new_name


def test_updating_non_existing_user(staff_user, user_repository):
    # Act
    staff_user.name = "new name"
    # Assert
    with pytest.raises(UserNotFoundError):
        user_repository.update_user(staff_user)
