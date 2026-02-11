from src.domain.entities.message import Message
from src.domain.errors import MessageNotFoundError
from src.domain.repositories.message_repository import IMessageRepository
from src.helpers.helpers import get_now


class InMemoryMessageRepository(IMessageRepository):
    def __init__(self):
        self.messages = {}

    def save(self, message: Message) -> Message:
        self.messages[message.id] = message
        return message

    def get_by_id(self, message_id: str) -> Message:
        message = self.messages.get(message_id)
        if message is None:
            raise MessageNotFoundError
        return message

    def get_by_external_id(self, external_id: str) -> Message | None:
        for message in self.messages.values():
            if message.external_id == external_id:
                return message
        return None

    def get_all(self) -> list[Message]:
        return list(self.messages.values())

    def delete(self, message_id: str) -> None:
        self.get_by_id(message_id=message_id)
        self.messages.pop(message_id)

    def mark_chat_messages_as_read(self, chat_id: str) -> int:
        updated_count = 0
        for message in self.messages.values():
            if message.chat_id == chat_id and not message.read:
                message.read = True
                message.updated_at = get_now()
                updated_count += 1
        return updated_count
