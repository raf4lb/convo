from datetime import UTC, datetime

import pytest

from src.application.exceptions import ReceiverContactDoesNotExistError
from src.application.use_cases.message_use_cases import (
    DeleteMessageUseCase,
    GetMessageUseCase,
    ReceiveMessageUseCase,
    UpdateMessageUseCase,
)
from src.domain.errors import ContactNotFoundError, MessageNotFoundError


def test_receive_message_use_case(
    message_repository,
    contact_repository,
    chat_repository,
    receiver_contact,
):
    # Arrange
    sender_phone_number = "5588999034445"
    sender_name = "Sender Name"
    message_external_id = "176273512356123"
    message_timestamp = datetime(2025, 11, 2, tzinfo=UTC)
    receiver_phone_number = receiver_contact.phone_number
    text = "Hello"

    use_case = ReceiveMessageUseCase(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )

    # Act
    message = use_case.execute(
        sender_phone_number=sender_phone_number,
        sender_name=sender_name,
        message_external_id=message_external_id,
        message_timestamp=message_timestamp,
        receiver_phone_number=receiver_phone_number,
        text=text,
    )

    # Assert
    fetched_message = message_repository.get_by_id(message.id)
    assert fetched_message.text == text


def test_receive_message_use_case_receiver_not_found(
    message_repository,
    contact_repository,
    chat_repository,
):
    # Arrange
    sender_phone_number = "5588999034445"
    sender_name = "Sender Name"
    message_external_id = "176273512356123"
    message_timestamp = datetime(2025, 11, 2, tzinfo=UTC)
    receiver_phone_number = "0000000000000"
    text = "Hello"
    use_case = ReceiveMessageUseCase(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )

    # Act/Assert
    with pytest.raises(ReceiverContactDoesNotExistError):
        use_case.execute(
            sender_phone_number=sender_phone_number,
            sender_name=sender_name,
            message_external_id=message_external_id,
            message_timestamp=message_timestamp,
            receiver_phone_number=receiver_phone_number,
            text=text,
        )


def test_receive_message_use_case_create_company_contact(
    receiver_contact,
    message_repository,
    contact_repository,
    chat_repository,
):
    # Arrange
    sender_phone_number = "5588999034446"
    sender_name = "Sender Name"
    message_external_id = "176273512356123"
    message_timestamp = datetime(2025, 11, 2, tzinfo=UTC)
    receiver_phone_number = receiver_contact.phone_number
    text = "Hello"
    use_case = ReceiveMessageUseCase(
        message_repository=message_repository,
        contact_repository=contact_repository,
        chat_repository=chat_repository,
    )

    with pytest.raises(ContactNotFoundError):
        contact_repository.get_company_contact_by_phone_number(
            company_id=receiver_contact.company_id,
            phone_number=sender_phone_number,
        )

    # Act
    use_case.execute(
        sender_phone_number=sender_phone_number,
        sender_name=sender_name,
        message_external_id=message_external_id,
        message_timestamp=message_timestamp,
        receiver_phone_number=receiver_phone_number,
        text=text,
    )

    # Assert
    fetched_contact = contact_repository.get_company_contact_by_phone_number(
        company_id=receiver_contact.company_id,
        phone_number=sender_phone_number,
    )
    assert fetched_contact.phone_number == sender_phone_number
    assert fetched_contact.name == sender_name


def test_get_message_use_case(message, message_repository):
    # Arrange
    use_case = GetMessageUseCase(message_repository=message_repository)

    # Act
    fetched_message = use_case.execute(message_id=message.id)

    # Assert
    assert fetched_message.id == message.id
    assert fetched_message.text == message.text


def test_update_message_use_case_existing_message(message, message_repository):
    # Arrange
    message_repository.save(message)
    use_case = UpdateMessageUseCase(message_repository=message_repository)

    # Act
    new_text = "New Text"
    use_case.execute(message_id=message.id, text=new_text)

    # Assert
    message = message_repository.get_by_id(message.id)
    assert message.text == new_text


def test_update_message_use_case_non_existing_message(message_repository):
    # Arrange
    use_case = UpdateMessageUseCase(message_repository=message_repository)

    # Act/Assert
    with pytest.raises(MessageNotFoundError):
        use_case.execute("message.id", "New Text")


def test_delete_message_use_case(message, message_repository):
    # Arrange
    use_case = DeleteMessageUseCase(message_repository=message_repository)

    # Act
    use_case.execute(message.id)

    # Act/Assert
    with pytest.raises(MessageNotFoundError):
        message_repository.get_by_id(message.id)
