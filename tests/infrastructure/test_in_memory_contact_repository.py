from src.infrastructure.repositories.in_memory_contact_repository import (
    InMemoryContactRepository,
)


def test_create_contact(contact):
    # Arrange
    repository = InMemoryContactRepository()

    # Act
    repository.save(contact)

    # Assert
    assert repository.get_contact_by_id(contact.id) is not None


def test_update_contact(contact):
    # Arrange
    repository = InMemoryContactRepository()
    repository.save(contact)

    # Act
    new_name = "New Name"
    contact.name = new_name
    repository.save(contact)

    # Assert
    contact = repository.get_contact_by_id(contact.id)
    assert contact.name == new_name
