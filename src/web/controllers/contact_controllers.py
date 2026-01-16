from src.application.use_cases.contact_use_cases import (
    CreateContactUseCase,
    GetCompanyContactsUseCase,
    GetContactUseCase,
)
from src.domain.entities.contact import Contact
from src.domain.errors import ContactNotFoundError
from src.web.controllers.interfaces import IContactHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


def format_contact(contact: Contact) -> dict:
    return {
        "id": contact.id,
        "name": contact.name,
        "phone_number": contact.phone_number,
        "email": contact.email,
        "company_id": contact.company_id,
        "is_blocked": contact.is_blocked,
        "created_at": contact.created_at.isoformat(),
        "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
    }


class CreateCompanyContactHttpController(IContactHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateContactUseCase(contact_repository=self._contact_repository)
        contact = use_case.execute(
            name=request.body["name"],
            phone_number=request.body["phone_number"],
            email=request.body.get("email"),
            company_id=request.body["company_id"],
        )

        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body=format_contact(contact),
        )


class GetContactHttpController(IContactHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetContactUseCase(contact_repository=self._contact_repository)
        try:
            contact = use_case.execute(contact_id=request.path_params["id"])
        except ContactNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "contact not found"},
            )

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=format_contact(contact),
        )


class GetCompanyContactsHttpController(IContactHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        company_id = request.path_params.get("company_id")
        use_case = GetCompanyContactsUseCase(
            contact_repository=self._contact_repository
        )
        contacts = use_case.execute(company_id=company_id)

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={"results": [format_contact(c) for c in contacts]},
        )
