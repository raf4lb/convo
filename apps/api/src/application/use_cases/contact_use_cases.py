from datetime import datetime

from src.application.interfaces import IContactUseCase
from src.domain.entities.base import UNSET, UnsetType
from src.domain.entities.contact import Contact
from src.helpers.helpers import generate_uuid4, get_now


class CreateContactUseCase(IContactUseCase):
    def execute(
        self,
        name: str,
        phone_number: str,
        email: str | None = None,
        company_id: str | None = None,
        tags: list[str] | None = None,
        notes: str | None = None,
    ) -> Contact:
        contact = Contact(
            id=generate_uuid4(),
            name=name,
            phone_number=phone_number,
            email=email,
            company_id=company_id,
            tags=[tag.lower() for tag in tags] if tags else [],
            notes=notes,
        )
        self._contact_repository.save(contact)
        return contact


class GetContactUseCase(IContactUseCase):
    def execute(self, contact_id: str) -> Contact:
        return self._contact_repository.get_by_id(contact_id)


class GetCompanyContactByPhoneUseCase(IContactUseCase):
    def execute(self, phone_number: str, company_id: str) -> Contact:
        return self._contact_repository.get_company_contact_by_phone_number(
            company_id, phone_number
        )


class UpdateContactUseCase(IContactUseCase):
    def execute(
        self,
        contact_id: str,
        name: str | UnsetType = UNSET,
        phone_number: str | UnsetType = UNSET,
        email: str | None | UnsetType = UNSET,
        company_id: str | None | UnsetType = UNSET,
        is_blocked: bool | UnsetType = UNSET,
        tags: list[str] | UnsetType = UNSET,
        notes: str | None | UnsetType = UNSET,
        last_contact_at: datetime | None | UnsetType = UNSET,
    ) -> Contact:
        contact = self._contact_repository.get_by_id(contact_id)

        if name is not UNSET:
            contact.name = name
        if phone_number is not UNSET:
            contact.phone_number = phone_number
        if email is not UNSET:
            contact.email = email
        if company_id is not UNSET:
            contact.company_id = company_id
        if is_blocked is not UNSET:
            contact.is_blocked = is_blocked
        if tags is not UNSET:
            contact.tags = [tag.lower() for tag in tags]
        if notes is not UNSET:
            contact.notes = notes
        if last_contact_at is not UNSET:
            contact.last_contact_at = last_contact_at

        contact.updated_at = get_now()
        self._contact_repository.save(contact)
        return contact


class DeleteContactUseCase(IContactUseCase):
    def execute(self, contact_id: str) -> None:
        self._contact_repository.delete(contact_id)


class GetCompanyContactsUseCase(IContactUseCase):
    def execute(self, company_id: str) -> list[Contact]:
        return self._contact_repository.get_by_company_id(company_id=company_id)


class SearchContactsUseCase(IContactUseCase):
    def execute(self, company_id: str, query: str) -> list[Contact]:
        return self._contact_repository.search_contacts(
            company_id=company_id, query=query
        )
