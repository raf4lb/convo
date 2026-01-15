from datetime import datetime

from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.domain.repositories.contact_repository import IContactRepository


class InMemoryContactRepository(IContactRepository):
    def __init__(self):
        self.contacts = {
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc085",
                company_id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Maria Silva",
                phone_number="+55 11 98765-4321",
                email="maria.silva@email.com",
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 12, 10, 30, 0),
                created_at=datetime(2024, 1, 10),
            ),
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc086",
                company_id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Carlos Santos",
                phone_number="+55 21 99876-5432",
                email="carlos.santos@email.com",
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 12, 9, 15, 0),
                created_at=datetime(2024, 2, 15),
            ),
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc087",
                company_id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Fernanda Lima",
                phone_number="+55 11 91234-5678",
                email=None,
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 11, 14, 20, 0),
                created_at=datetime(2024, 3, 20),
            ),
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc088",
                company_id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Pedro Oliveira",
                phone_number="+55 11 98888-7777",
                email="pedro.oliveira@email.com",
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 11, 16, 45, 0),
                created_at=datetime(2024, 4, 5),
            ),
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc089",
                company_id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Julia Costa",
                phone_number="+55 21 97777-6666",
                email="julia.costa@email.com",
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 12, 11, 45, 0),
                created_at=datetime(2024, 5, 12),
            ),
            "e7fc687a-e0fa-49ea-af1b-7a2a2e6fc090": Contact(
                id="e7fc687a-e0fa-49ea-af1b-7a2a2e6fc090",
                company_id="6dfaada5-37b1-442d-a21b-b63edf12bbd0",
                name="Roberto Alves",
                phone_number="+55 11 95555-4444",
                email="roberto.alves@email.com",
                is_blocked=False,
                last_contact_at=datetime(2024, 11, 10, 10, 0, 0),
                created_at=datetime(2024, 2, 25),
            ),
        }

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
        self.get_by_id(contact_id=contact_id)
        self.contacts.pop(contact_id)

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
