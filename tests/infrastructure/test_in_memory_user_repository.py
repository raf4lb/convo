from src.infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


def test_create_user(staff_user):
    # Arrange
    repository = InMemoryUserRepository()

    # Act
    repository.save(staff_user)

    # Assert
    assert repository.get_user_by_id(staff_user.id) is not None


def test_update_user(staff_user):
    # Arrange
    repository = InMemoryUserRepository()
    repository.save(staff_user)

    # Act
    new_name = "New Name"
    staff_user.name = new_name
    repository.save(staff_user)

    # Assert
    user = repository.get_user_by_id(staff_user.id)
    assert user.name == new_name
