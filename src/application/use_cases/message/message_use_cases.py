import uuid

from src.application.interfaces.use_case_interface import IUseCase
from src.domain.entities.message import Message
from src.domain.repositories.message_repository import IMessageRepository
from src.helpers.helpes import get_now_iso_format


class CreateMessageUseCase(IUseCase):
    def __init__(self, repository: IMessageRepository):
        self._repository = repository

    def execute(
        self,
        company_id: str,
        sender_id: str,
        receiver_id: str,
        received: bool,
        text: str,
    ) -> Message:
        created_at = get_now_iso_format()
        message = Message(
            id=str(uuid.uuid4()),
            company_id=company_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            received=received,
            text=text,
            created_at=created_at,
            updated_at=created_at,
        )
        self._repository.save(message)
        return message


class UpdateMessageUseCase(IUseCase):
    def __init__(self, repository: IMessageRepository):
        self._repository = repository

    def execute(self, message_id: str, text: str) -> Message:
        message = self._repository.get_message_by_id(message_id)
        message.text = text
        message.updated_at = get_now_iso_format()
        self._repository.save(message)
        return message
