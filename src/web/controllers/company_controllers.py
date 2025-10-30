from src.application.use_cases.company.company_use_cases import (
    CreateCompanyUseCase,
    UpdateCompanyUseCase,
)
from src.domain.repositories.company_repository import ICompanyRepository
from src.web.controllers.http_types import HttpRequest, HttpResponse, StatusCodes


class CompanyController:
    def __init__(self, company_repository: ICompanyRepository):
        self._repository = company_repository


class CreateCompanyHTTPController(CompanyController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = CreateCompanyUseCase(repository=self._repository)
        user = use_case.execute(
            name=request.body["name"],
        )
        return HttpResponse(
            status_code=StatusCodes.CREATED.value,
            body={
                "id": user.id,
                "name": user.name,
            },
        )


class UpdateCompanyHTTPController(CompanyController):
    def handle(self, request: HttpRequest) -> HttpResponse:
        use_case = UpdateCompanyUseCase(repository=self._repository)
        user = use_case.execute(
            company_id=request.path_params["id"],
            name=request.body["name"],
        )
        return HttpResponse(
            status_code=StatusCodes.OK.value,
            body={
                "id": user.id,
                "name": user.name,
            },
        )
