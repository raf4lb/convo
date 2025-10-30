from src.domain.entities.message import Message
from src.domain.errors import MessageNotFoundError
from src.domain.repositories.message_repository import IMessageRepository


class InMemoryMessageRepository(IMessageRepository):
    def __init__(self):
        self.messages = {}

    def save(self, message: Message) -> None:
        self.messages[message.id] = message

    def get_by_id(self, message_id: str) -> Message | None:
        message = self.messages.get(message_id)
        if message is None:
            raise MessageNotFoundError
        return message

    def get_messages(self) -> list[Message]:
        return list(self.messages.values())

    def delete(self, message_id: str) -> None:
        try:
            self.messages.pop(message_id)
        except KeyError:
            raise MessageNotFoundError
