from src.application.interfaces.use_case_interface import UseCaseInterface
from src.application.interfaces.user_repository_interface import (
    CompanyRepositoryInterface,
)
from src.domain.entities.company import Company


class CreateCompanyUseCase(UseCaseInterface):
    def __init__(self, repository: CompanyRepositoryInterface):
        self._repository = repository

    def execute(self, company: Company) -> None:
        self._repository.create_company(company)


class UpdateCompanyUseCase(UseCaseInterface):
    def __init__(self, repository: CompanyRepositoryInterface):
        self._repository = repository

    def execute(self, company: Company) -> None:
        self._repository.update_company(company)
