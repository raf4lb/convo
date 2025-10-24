import uuid

from src.application.exceptions import CompanyNotFoundError
from src.application.interfaces.user_repository_interface import (
    CompanyRepositoryInterface,
)
from src.domain.entities.company import Company


class InMemoryCompanyRepository(CompanyRepositoryInterface):
    def __init__(self):
        self.companies = {}

    def create_company(self, company: Company) -> None:
        self.companies[company.id] = company

    def update_company(self, company: Company) -> None:
        if company.id not in self.companies:
            raise CompanyNotFoundError(f"company {company.id} not found")
        self.companies[company.id] = company

    def get_company_by_id(self, company_id: uuid.UUID) -> Company:
        return self.companies.get(company_id)

    def get_companies(self) -> list[Company]:
        return list(self.companies.values())
