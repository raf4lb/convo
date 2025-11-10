from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.domain.repositories.contact_repository import IContactRepository


class InMemoryContactRepository(IContactRepository):
    def __init__(self):
        self.contacts = {}

    def save(self, contact: Contact) -> Contact:
        self.contacts[contact.id] = contact
        return contact

    def get_by_id(self, contact_id: str) -> Contact | None:
        contact = self.contacts.get(contact_id)
        if contact is None:
            raise ContactNotFoundError
        return contact

    def get_all(self) -> list[Contact]:
        return list(self.contacts.values())

    def delete(self, contact_id: str) -> None:
        self.contacts.pop(contact_id, None)

    def get_by_phone_number(self, phone_number: str) -> Contact | None:
        for contact in self.contacts.values():
            if contact.phone_number == phone_number:
                return contact
        return None

    def get_company_contact_by_phone_number(
        self,
        company_id: str,
        phone_number: str,
    ) -> Contact | None:
        for contact in self.contacts.values():
            if (
                contact.company_id == company_id
                and contact.phone_number == phone_number
            ):
                return contact
        return None
