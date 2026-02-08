from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.domain.repositories.contact_repository import IContactRepository
from src.infrastructure.daos.postgres_contact_dao import PostgresContactDAO


class PostgresContactRepository(IContactRepository):
    def __init__(self, contact_dao: PostgresContactDAO):
        self._contact_dao = contact_dao

    @staticmethod
    def _parse_row(row: tuple) -> Contact:
        return Contact(
            id=row[0],
            name=row[1],
            phone_number=row[2],
            email=row[3],
            company_id=row[4],
            is_blocked=row[5],
            tags=row[6].split(",") if row[6] else [],
            notes=row[7],
            last_contact_at=row[8],
            created_at=row[9],
            updated_at=row[10],
        )

    def save(self, contact: Contact) -> None:
        existing = self._contact_dao.get_by_id(contact_id=contact.id)
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "phone_number": contact.phone_number,
            "email": contact.email,
            "company_id": contact.company_id,
            "is_blocked": contact.is_blocked,
            "tags": ",".join(contact.tags) if contact.tags else None,
            "notes": contact.notes,
            "last_contact_at": contact.last_contact_at,
            "updated_at": contact.updated_at,
        }

        if existing:
            self._contact_dao.update(contact_data)
        else:
            self._contact_dao.insert(contact_data)

    def get_by_id(self, contact_id: str) -> Contact:
        row = self._contact_dao.get_by_id(contact_id=contact_id)
        if not row:
            raise ContactNotFoundError

        return self._parse_row(row=row)

    def get_by_company_id(self, company_id: str) -> list[Contact]:
        rows = self._contact_dao.get_by_company_id(company_id=company_id)
        return [self._parse_row(row=row) for row in rows]

    def get_by_phone_number(self, phone_number: str) -> Contact:
        row = self._contact_dao.get_by_phone_number(phone_number=phone_number)
        if not row:
            raise ContactNotFoundError

        return self._parse_row(row=row)

    def get_company_contact_by_phone_number(
        self, company_id: str, phone_number: str
    ) -> Contact:
        row = self._contact_dao.get_company_contact_by_phone_number(
            company_id=company_id, phone_number=phone_number
        )
        if not row:
            raise ContactNotFoundError

        return self._parse_row(row=row)

    def get_all(self) -> list[Contact]:
        rows = self._contact_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def search_contacts(self, company_id: str, query: str) -> list[Contact]:
        rows = self._contact_dao.search_contacts(company_id=company_id, query=query)
        return [self._parse_row(row=row) for row in rows]

    def delete(self, contact_id: str) -> None:
        self.get_by_id(contact_id=contact_id)
        self._contact_dao.delete(contact_id=contact_id)
