from abc import ABC, abstractmethod

from src.domain.entities.message import Message


class IMessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message) -> Message: ...

    @abstractmethod
    def get_by_id(self, message_id: str) -> Message: ...

    @abstractmethod
    def get_all(self) -> list[Message]: ...

    @abstractmethod
    def delete(self, message_id: str) -> None: ...
