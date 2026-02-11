from datetime import UTC, datetime

import pytest

from src.application.exceptions import ReceiverContactDoesNotExistError
from src.application.use_cases.message_use_cases import (
    DeleteMessageUseCase,
    GetMessageUseCase,
    MarkChatAsReadUseCase,
    ReceiveMessageUseCase,
    UpdateMessageUseCase,
)
from src.domain.entities.message import Message
from src.domain.errors import ContactNotFoundError, MessageNotFoundError
from tests.fakes.repositories.fake_in_memory_message_repository import (
    InMemoryMessageRepository,
)


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


def test_receive_message_defaults_to_unread(
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
    assert message.read is False


def test_message_entity_with_read_field():
    # Arrange & Act
    message = Message(
        id="msg-1",
        external_id="ext-123",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Test",
        read=True,
    )

    # Assert
    assert message.read is True


def test_message_entity_read_defaults_to_false():
    # Arrange & Act
    message = Message(
        id="msg-1",
        external_id="ext-123",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Test",
    )

    # Assert
    assert message.read is False


def test_mark_chat_as_read_use_case():
    # Arrange
    fake_repo = InMemoryMessageRepository()

    # Create messages: 2 unread, 1 already read
    message1 = Message(
        id="msg-1",
        external_id="ext-1",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Unread message 1",
        read=False,
    )
    message2 = Message(
        id="msg-2",
        external_id="ext-2",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Unread message 2",
        read=False,
    )
    message3 = Message(
        id="msg-3",
        external_id="ext-3",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Already read message",
        read=True,
    )

    fake_repo.save(message1)
    fake_repo.save(message2)
    fake_repo.save(message3)

    use_case = MarkChatAsReadUseCase(message_repository=fake_repo)

    # Act
    updated_count = use_case.execute(chat_id="chat-1")

    # Assert
    assert updated_count == 2  # Only 2 were unread

    # Verify messages were actually marked as read
    msg1 = fake_repo.get_by_id("msg-1")
    msg2 = fake_repo.get_by_id("msg-2")
    msg3 = fake_repo.get_by_id("msg-3")

    assert msg1.read is True
    assert msg2.read is True
    assert msg3.read is True  # Was already read
    assert msg1.updated_at is not None
    assert msg2.updated_at is not None


def test_mark_chat_as_read_when_all_already_read():
    # Arrange
    fake_repo = InMemoryMessageRepository()

    message = Message(
        id="msg-1",
        external_id="ext-1",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Already read",
        read=True,
    )
    fake_repo.save(message)

    use_case = MarkChatAsReadUseCase(message_repository=fake_repo)

    # Act
    updated_count = use_case.execute(chat_id="chat-1")

    # Assert
    assert updated_count == 0  # No updates needed


def test_mark_chat_as_read_only_affects_target_chat():
    # Arrange
    fake_repo = InMemoryMessageRepository()

    # Chat 1 message
    message1 = Message(
        id="msg-1",
        external_id="ext-1",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Chat 1 message",
        read=False,
    )
    # Chat 2 message
    message2 = Message(
        id="msg-2",
        external_id="ext-2",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-2",
        text="Chat 2 message",
        read=False,
    )

    fake_repo.save(message1)
    fake_repo.save(message2)

    use_case = MarkChatAsReadUseCase(message_repository=fake_repo)

    # Act
    updated_count = use_case.execute(chat_id="chat-1")

    # Assert
    assert updated_count == 1  # Only 1 message in chat-1

    # Verify chat-1 message is read
    msg1 = fake_repo.get_by_id("msg-1")
    assert msg1.read is True

    # Chat 2 message should still be unread
    msg2 = fake_repo.get_by_id("msg-2")
    assert msg2.read is False


def test_fake_repository_mark_chat_messages_as_read():
    # Arrange
    fake_repo = InMemoryMessageRepository()

    message1 = Message(
        id="msg-1",
        external_id="ext-1",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Chat 1 unread message",
        read=False,
    )
    message2 = Message(
        id="msg-2",
        external_id="ext-2",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-1",
        text="Chat 1 already read",
        read=True,
    )
    message3 = Message(
        id="msg-3",
        external_id="ext-3",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id="chat-2",
        text="Chat 2 message",
        read=False,
    )

    fake_repo.save(message1)
    fake_repo.save(message2)
    fake_repo.save(message3)

    # Act
    updated_count = fake_repo.mark_chat_messages_as_read("chat-1")

    # Assert
    assert updated_count == 1  # Only msg-1 was unread

    # Verify state changes
    msg1 = fake_repo.get_by_id("msg-1")
    msg2 = fake_repo.get_by_id("msg-2")
    msg3 = fake_repo.get_by_id("msg-3")

    assert msg1.read is True
    assert msg1.updated_at is not None
    assert msg2.read is True  # Still read
    assert msg3.read is False  # Different chat, unchanged
