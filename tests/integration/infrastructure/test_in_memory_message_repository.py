import pytest

from src.domain.errors import MessageNotFoundError
from src.infrastructure.repositories.in_memory_message_repository import (
    InMemoryMessageRepository,
)


def test_create_message(message):
    # Arrange
    repository = InMemoryMessageRepository()

    # Act
    repository.save(message)

    # Assert
    assert repository.get_by_id(message.id) is not None


def test_update_message(message):
    # Arrange
    repository = InMemoryMessageRepository()
    repository.save(message)

    # Act
    new_text = "New Text"
    message.text = new_text
    repository.save(message)

    # Assert
    message = repository.get_by_id(message.id)
    assert message.text == new_text


def test_delete_message(message):
    # Arrange
    repository = InMemoryMessageRepository()
    repository.save(message)

    # Act
    repository.delete(message.id)

    # Assert
    with pytest.raises(MessageNotFoundError):
        repository.get_by_id(message.id)
