from abc import ABC, abstractmethod

from src.domain.entities.contact import Contact


class IContactRepository(ABC):
    @abstractmethod
    def save(self, contact: Contact) -> None: ...

    @abstractmethod
    def get_by_id(self, contact_id: str) -> Contact | None: ...

    @abstractmethod
    def get_contacts(self) -> list[Contact]: ...

    @abstractmethod
    def delete(self, contact_id: str) -> None: ...
