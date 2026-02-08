from datetime import UTC, datetime

from src.domain.entities.message import Message
from src.helpers.helpers import generate_uuid4


def test_is_from_contact_returns_true_when_sent_by_user_id_is_none():
    message = Message(
        id=generate_uuid4(),
        external_id="wamid.test123",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id=generate_uuid4(),
        text="Hello from contact",
        sent_by_user_id=None,
    )

    assert message.is_from_contact() is True
    assert message.is_from_user() is False


def test_is_from_user_returns_true_when_sent_by_user_id_has_value():
    user_id = generate_uuid4()
    message = Message(
        id=generate_uuid4(),
        external_id="wamid.test456",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id=generate_uuid4(),
        text="Hello from user",
        sent_by_user_id=user_id,
    )

    assert message.is_from_contact() is False
    assert message.is_from_user() is True


def test_message_creation_with_no_sender_defaults_to_contact():
    message = Message(
        id=generate_uuid4(),
        external_id="wamid.test789",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id=generate_uuid4(),
        text="Default message",
    )

    assert message.sent_by_user_id is None
    assert message.is_from_contact() is True


def test_message_creation_with_user_sender():
    user_id = generate_uuid4()
    message = Message(
        id=generate_uuid4(),
        external_id="wamid.test101",
        external_timestamp=datetime(2025, 11, 2, tzinfo=UTC),
        chat_id=generate_uuid4(),
        text="User sent message",
        sent_by_user_id=user_id,
    )

    assert message.sent_by_user_id == user_id
    assert message.is_from_user() is True
