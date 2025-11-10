from src.application.use_cases.contact_use_cases import (
    CreateContactUseCase,
    GetContactUseCase,
)
from src.domain.errors import ContactNotFoundError
from src.web.controllers.http_types import HttpRequest, HttpResponse, StatusCodes
from src.web.controllers.interfaces import IContactHttpController


class CreateCompanyContactHttpController(IContactHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateContactUseCase(contact_repository=self._contact_repository)
        contact = use_case.execute(
            name=request.body["name"],
            phone_number=request.body["phone_number"],
            company_id=request.body["company_id"],
        )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": contact.id,
                "name": contact.name,
                "phone_number": contact.phone_number,
                "company_id": contact.company_id,
                "created_at": contact.created_at.isoformat(),
                "updated_at": contact.updated_at.isoformat()
                if contact.updated_at
                else None,
            },
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
            body={
                "id": contact.id,
                "name": contact.name,
                "phone_number": contact.phone_number,
                "company_id": contact.company_id,
                "created_at": contact.created_at.isoformat(),
                "updated_at": contact.updated_at.isoformat()
                if contact.updated_at
                else None,
            },
        )
