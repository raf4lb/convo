from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.domain.repositories.contact_repository import IContactRepository
from src.infrastructure.daos.contact_dao import SQLiteContactDAO


class SQLiteContactRepository(IContactRepository):
    def __init__(self, contact_dao: SQLiteContactDAO):
        self._contact_dao = contact_dao

    @staticmethod
    def _parse_row(row: tuple) -> Contact:
        return Contact(
            id=row[0],
            name=row[1],
            phone_number=row[2],
            email=row[3],
            company_id=row[4],
            is_blocked=bool(row[5]),
            last_contact_at=row[6],
            created_at=row[7],
            updated_at=row[8],
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
            "last_contact_at": contact.last_contact_at,
            "updated_at": contact.updated_at,
        }

        if existing:
            self._contact_dao.update(contact_data)
        else:
            self._contact_dao.insert(contact_data)

    def get_by_id(self, contact_id: str) -> Contact | None:
        row = self._contact_dao.get_by_id(contact_id=contact_id)
        if not row:
            raise ContactNotFoundError

        return self._parse_row(row=row)

    def get_by_phone_number(self, phone_number: str) -> Contact | None:
        row = self._contact_dao.get_by_phone_number(phone_number=phone_number)
        if not row:
            return None

        return self._parse_row(row=row)

    def get_company_contact_by_phone_number(
        self, company_id: str, phone_number: str
    ) -> Contact | None:
        row = self._contact_dao.get_company_contact_by_phone_number(
            company_id=company_id, phone_number=phone_number
        )
        if not row:
            return None

        return self._parse_row(row=row)

    def get_all(self) -> list[Contact]:
        rows = self._contact_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, contact_id: str) -> None:
        self.get_by_id(contact_id=contact_id)
        self._contact_dao.delete(contact_id=contact_id)
