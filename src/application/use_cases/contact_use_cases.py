from src.application.interfaces import IContactUseCase
from src.domain.entities.contact import Contact
from src.helpers.helpers import generate_uuid4, get_now


class CreateContactUseCase(IContactUseCase):
    def execute(
        self,
        name: str,
        phone_number: str,
        company_id: str | None = None,
    ) -> Contact:
        contact = Contact(
            id=generate_uuid4(),
            name=name,
            phone_number=phone_number,
            company_id=company_id,
        )
        self._contact_repository.save(contact)
        return contact


class GetContactUseCase(IContactUseCase):
    def execute(self, contact_id: str) -> Contact:
        return self._contact_repository.get_by_id(contact_id)


class UpdateContactUseCase(IContactUseCase):
    def execute(
        self,
        contact_id: str,
        name: str,
        phone_number: str,
        company_id: str | None = None,
    ) -> Contact:
        contact = self._contact_repository.get_by_id(contact_id)
        contact.company_id = company_id
        contact.name = name
        contact.phone_number = phone_number
        contact.updated_at = get_now()
        self._contact_repository.save(contact)
        return contact


class DeleteContactUseCase(IContactUseCase):
    def execute(self, contact_id: str) -> None:
        self._contact_repository.delete(contact_id)
