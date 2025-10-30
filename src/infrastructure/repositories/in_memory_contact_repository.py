from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.domain.repositories.contact_repository import IContactRepository


class InMemoryContactRepository(IContactRepository):
    def __init__(self):
        self.contacts = {}

    def save(self, contact: Contact) -> None:
        self.contacts[contact.id] = contact

    def get_by_id(self, contact_id: str) -> Contact | None:
        contact = self.contacts.get(contact_id)
        if contact is None:
            raise ContactNotFoundError
        return contact

    def get_contacts(self) -> list[Contact]:
        return list(self.contacts.values())

    def delete(self, contact_id: str) -> None:
        try:
            self.contacts.pop(contact_id)
        except KeyError:
            raise ContactNotFoundError
