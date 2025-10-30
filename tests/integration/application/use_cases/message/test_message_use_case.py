import uuid

import pytest

from src.application.use_cases.message.message_use_cases import (
    CreateMessageUseCase,
    DeleteMessageUseCase,
    UpdateMessageUseCase,
)
from src.domain.errors import MessageNotFoundError


def test_create_message_use_case(message_repository):
    # Arrange
    use_case = CreateMessageUseCase(repository=message_repository)

    # Act
    user = use_case.execute(
        company_id=str(uuid.uuid4()),
        sender_id=str(uuid.uuid4()),
        receiver_id=str(uuid.uuid4()),
        received=True,
        text="Text",
    )

    # Assert
    assert message_repository.get_by_id(user.id) is not None


def test_update_message_use_case_existing_user(message, message_repository):
    # Arrange
    message_repository.save(message)
    use_case = UpdateMessageUseCase(repository=message_repository)

    # Act
    new_text = "New Text"
    use_case.execute(message_id=message.id, text=new_text)

    # Assert
    message = message_repository.get_by_id(message.id)
    assert message.text == new_text


def test_update_user_use_case_non_existing_user(message, message_repository):
    # Arrange
    use_case = UpdateMessageUseCase(repository=message_repository)

    # Act/Assert
    with pytest.raises(MessageNotFoundError):
        use_case.execute(message.id, "New Text")


def test_delete_message_use_case(message, message_repository):
    # Arrange
    message_repository.save(message)
    use_case = DeleteMessageUseCase(repository=message_repository)

    # Act
    use_case.execute(message.id)

    # Act/Assert
    with pytest.raises(MessageNotFoundError):
        message_repository.get_by_id(message.id)
