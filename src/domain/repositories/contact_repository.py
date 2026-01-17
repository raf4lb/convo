from abc import ABC, abstractmethod

from src.domain.entities.contact import Contact


class IContactRepository(ABC):
    @abstractmethod
    def save(self, contact: Contact) -> Contact: ...

    @abstractmethod
    def get_by_id(self, contact_id: str) -> Contact: ...

    @abstractmethod
    def get_all(self) -> list[Contact]: ...

    @abstractmethod
    def delete(self, contact_id: str) -> None: ...

    @abstractmethod
    def get_by_company_id(self, company_id: str) -> list[Contact]: ...

    @abstractmethod
    def get_by_phone_number(self, phone_number: str) -> Contact: ...

    @abstractmethod
    def get_company_contact_by_phone_number(
        self,
        company_id: str,
        phone_number: str,
    ) -> Contact: ...

    @abstractmethod
    def search_contacts(self, company_id: str, query: str) -> list[Contact]: ...
