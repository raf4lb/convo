from datetime import datetime

from src.application.exceptions import ReceiverContactDoesNotExistError
from src.application.interfaces import IMessageUseCase
from src.domain.entities.chat import Chat
from src.domain.entities.contact import Contact
from src.domain.entities.message import Message
from src.domain.errors import ChatNotFoundError, ContactNotFoundError
from src.domain.repositories.chat_repository import IChatRepository
from src.domain.repositories.contact_repository import IContactRepository
from src.domain.repositories.message_repository import IMessageRepository
from src.helpers.helpers import generate_uuid4, get_now


class ReceiveMessageUseCase(IMessageUseCase):
    def __init__(
        self,
        message_repository: IMessageRepository,
        contact_repository: IContactRepository,
        chat_repository: IChatRepository,
    ):
        super().__init__(message_repository=message_repository)
        self._contact_repository = contact_repository
        self._chat_repository = chat_repository

    def execute(
        self,
        sender_phone_number: str,
        sender_name: str,
        message_external_id: str,
        message_timestamp: datetime,
        receiver_phone_number: str,
        text: str,
    ) -> Message:
        # Check for existing message (idempotency)
        existing_message = self._message_repository.get_by_external_id(
            external_id=message_external_id
        )
        if existing_message:
            return existing_message

        try:
            receiver_contact = self._contact_repository.get_by_phone_number(
                phone_number=receiver_phone_number
            )
        except ContactNotFoundError:
            raise ReceiverContactDoesNotExistError

        try:
            sender_contact = (
                self._contact_repository.get_company_contact_by_phone_number(
                    company_id=receiver_contact.company_id,
                    phone_number=sender_phone_number,
                )
            )
        except ContactNotFoundError:
            sender_contact = Contact(
                id=generate_uuid4(),
                name=sender_name,
                phone_number=sender_phone_number,
                company_id=receiver_contact.company_id,
            )
            sender_contact = self._contact_repository.save(sender_contact)

        try:
            chat = self._chat_repository.get_company_chat_by_contact_id(
                company_id=receiver_contact.company_id,
                contact_id=sender_contact.id,
            )
        except ChatNotFoundError:
            chat = Chat(
                id=generate_uuid4(),
                company_id=receiver_contact.company_id,
                contact_id=sender_contact.id,
            )
            chat = self._chat_repository.save(chat)

        message = Message(
            id=generate_uuid4(),
            external_id=message_external_id,
            external_timestamp=message_timestamp,
            chat_id=chat.id,
            sent_by_user_id=None,  # Message is from contact
            text=text,
            read=False,  # Incoming messages are unread by default
        )
        saved_message = self._message_repository.save(message)
        return saved_message


class GetMessageUseCase(IMessageUseCase):
    def execute(self, message_id: str) -> Message:
        return self._message_repository.get_by_id(message_id)


class UpdateMessageUseCase(IMessageUseCase):
    def execute(self, message_id: str, text: str) -> Message:
        message = self._message_repository.get_by_id(message_id)
        message.text = text
        message.updated_at = get_now()
        self._message_repository.save(message)
        return message


class DeleteMessageUseCase(IMessageUseCase):
    def execute(self, message_id: str) -> None:
        self._message_repository.delete(message_id)


class MarkChatAsReadUseCase(IMessageUseCase):
    def execute(self, chat_id: str) -> int:
        updated_count = self._message_repository.mark_chat_messages_as_read(chat_id)
        return updated_count


class GetChatMessagesUseCase(IMessageUseCase):
    def execute(self, chat_id: str) -> list[Message]:
        return self._message_repository.get_by_chat_id(chat_id=chat_id)


class SendMessageUseCase(IMessageUseCase):
    def execute(
        self,
        chat_id: str,
        text: str,
        sent_by_user_id: str,
        external_id: str | None = None,
        external_timestamp: datetime | None = None,
    ) -> Message:
        # For user-sent messages, generate an external_id if not provided
        if not external_id:
            external_id = f"user_msg_{generate_uuid4()}"
        if not external_timestamp:
            external_timestamp = get_now()

        message = Message(
            id=generate_uuid4(),
            external_id=external_id,
            external_timestamp=external_timestamp,
            chat_id=chat_id,
            text=text,
            sent_by_user_id=sent_by_user_id,
            read=True,  # User-sent messages are marked as read
        )
        return self._message_repository.save(message)
