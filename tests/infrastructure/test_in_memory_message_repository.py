from src.infrastructure.repositories.in_memory_message_repository import (
    InMemoryMessageRepository,
)


def test_create_message(message):
    # Arrange
    repository = InMemoryMessageRepository()

    # Act
    repository.save(message)

    # Assert
    assert repository.get_message_by_id(message.id) is not None


def test_update_message(message):
    # Arrange
    repository = InMemoryMessageRepository()
    repository.save(message)

    # Act
    new_text = "New Text"
    message.text = new_text
    repository.save(message)

    # Assert
    message = repository.get_message_by_id(message.id)
    assert message.text == new_text
