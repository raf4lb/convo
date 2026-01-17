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
            received_by=chat.attached_user_id,
            is_received=True,
            text=text,
        )
        self._message_repository.save(message)
        return message


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
