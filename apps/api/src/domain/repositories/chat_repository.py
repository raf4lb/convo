from abc import ABC, abstractmethod

from src.domain.entities.chat import Chat


class IChatRepository(ABC):
    @abstractmethod
    def save(self, chat: Chat) -> Chat: ...

    @abstractmethod
    def get_by_id(self, chat_id: str) -> Chat: ...

    @abstractmethod
    def get_all(self) -> list[Chat]: ...

    @abstractmethod
    def get_by_company_id(self, company_id: str) -> list[Chat]: ...

    @abstractmethod
    def get_company_chat_by_contact_id(
        self,
        company_id: str,
        contact_id: str,
    ) -> Chat: ...

    @abstractmethod
    def delete(self, chat_id: str) -> None: ...

    @abstractmethod
    def get_unassigned_by_company_id(self, company_id: str) -> list[Chat]: ...

    @abstractmethod
    def get_by_attendant_id(self, company_id: str, attendant_id: str) -> list[Chat]: ...

    @abstractmethod
    def search_chats(
        self, company_id: str, query: str, user_id: str | None = None
    ) -> list[Chat]: ...
