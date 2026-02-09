from src.application.use_cases.company_use_cases import (
    CreateCompanyUseCase,
    DeleteCompanyUseCase,
    GetCompanyUseCase,
    ListCompanyUseCase,
    UpdateCompanyUseCase,
)
from src.domain.entities.company import Company
from src.domain.errors import CompanyNotFoundError
from src.web.controllers.interfaces import ICompanyHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


def format_company(company: Company) -> dict:
    return {
        "id": company.id,
        "name": company.name,
        "email": company.email,
        "phone": company.phone,
        "is_active": company.is_active,
        "attendant_sees_all_conversations": company.attendant_sees_all_conversations,
        "whatsapp_api_key": company.whatsapp_api_key,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "updated_at": company.updated_at.isoformat() if company.updated_at else None,
    }


class CreateCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateCompanyUseCase(company_repository=self._repository)
        company = use_case.execute(
            name=request.body["name"],
            email=request.body["email"],
            phone=request.body["phone"],
            is_active=request.body.get("is_active"),
            attendant_sees_all_conversations=request.body.get(
                "attendant_sees_all_conversations"
            ),
            whatsapp_api_key=request.body.get("whatsapp_api_key"),
        )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body=format_company(company),
        )


class GetCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = GetCompanyUseCase(company_repository=self._repository)
        try:
            company = use_case.execute(company_id=request.path_params["id"])
        except CompanyNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "company not found"},
            )
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=format_company(company),
        )


class UpdateCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = UpdateCompanyUseCase(company_repository=self._repository)
        kwargs = {
            "company_id": request.path_params["id"],
            "name": request.body["name"],
            "email": request.body["email"],
            "phone": request.body["phone"],
        }

        # Only include optional fields if present in request
        if "is_active" in request.body:
            kwargs["is_active"] = request.body["is_active"]
        if "attendant_sees_all_conversations" in request.body:
            kwargs["attendant_sees_all_conversations"] = request.body[
                "attendant_sees_all_conversations"
            ]
        if "whatsapp_api_key" in request.body:
            kwargs["whatsapp_api_key"] = request.body["whatsapp_api_key"]

        company = use_case.execute(**kwargs)

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=format_company(company),
        )


class DeleteCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = DeleteCompanyUseCase(company_repository=self._repository)
        try:
            use_case.execute(company_id=request.path_params["id"])
        except CompanyNotFoundError:
            return HttpResponse(
                status_code=StatusCodes.NOT_FOUND.value,
                body={"detail": "company not found"},
            )
        return HttpResponse(status_code=StatusCodes.NO_CONTENT.value)


class ListCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = ListCompanyUseCase(company_repository=self._repository)
        companies = use_case.execute()
        body = {
            "results": [format_company(company) for company in companies],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )
