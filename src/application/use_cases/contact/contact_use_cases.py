import uuid

from src.application.interfaces.use_case_interface import IUseCase
from src.domain.entities.contact import Contact
from src.domain.repositories.contact_repository import IContactRepository
from src.helpers.helpes import get_now_iso_format


class CreateContactUseCase(IUseCase):
    def __init__(self, repository: IContactRepository):
        self._repository = repository

    def execute(
        self,
        name: str,
        phone_number: str,
        company_id: str | None = None,
    ) -> Contact:
        created_at = get_now_iso_format()
        contact = Contact(
            id=str(uuid.uuid4()),
            name=name,
            phone_number=phone_number,
            company_id=company_id,
            created_at=created_at,
            updated_at=created_at,
        )
        self._repository.save(contact)
        return contact


class UpdateContactUseCase(IUseCase):
    def __init__(self, repository: IContactRepository):
        self._repository = repository

    def execute(
        self,
        contact_id: str,
        name: str,
        phone_number: str,
        company_id: str | None = None,
    ) -> Contact:
        contact = self._repository.get_contact_by_id(contact_id)
        contact.company_id = company_id
        contact.name = name
        contact.phone_number = phone_number
        contact.updated_at = get_now_iso_format()
        self._repository.save(contact)
        return contact
