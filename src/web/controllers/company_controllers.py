from src.application.use_cases.company_use_cases import (
    CreateCompanyUseCase,
    DeleteCompanyUseCase,
    GetCompanyUseCase,
    ListCompanyUseCase,
    UpdateCompanyUseCase,
)
from src.domain.errors import CompanyNotFoundError
from src.web.controllers.interfaces import ICompanyHttpController
from src.web.http_types import HttpRequest, HttpResponse, StatusCodes


class CreateCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateCompanyUseCase(company_repository=self._repository)
        company = use_case.execute(
            name=request.body["name"],
        )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": company.id,
                "name": company.name,
                "created_at": company.created_at.isoformat(),
                "updated_at": company.updated_at.isoformat()
                if company.updated_at
                else None,
            },
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
            body={
                "id": company.id,
                "name": company.name,
            },
        )


class UpdateCompanyHttpController(ICompanyHttpController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = UpdateCompanyUseCase(company_repository=self._repository)
        company = use_case.execute(
            company_id=request.path_params["id"],
            name=request.body["name"],
        )
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": company.id,
                "name": company.name,
            },
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
            "companies": [
                {
                    "id": company.id,
                    "name": company.name,
                }
                for company in companies
            ],
        }

        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body=body,
        )
