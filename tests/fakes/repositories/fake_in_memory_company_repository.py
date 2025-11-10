from src.domain.entities.company import Company
from src.domain.errors import CompanyNotFoundError
from src.domain.repositories.company_repository import (
    ICompanyRepository,
)


class InMemoryCompanyRepository(ICompanyRepository):
    def __init__(self):
        self.companies = {}

    def save(self, company: Company) -> Company:
        self.companies[company.id] = company
        return company

    def get_by_id(self, company_id: str) -> Company | None:
        company = self.companies.get(company_id)
        if company is None:
            raise CompanyNotFoundError
        return company

    def get_all(self) -> list[Company]:
        return list(self.companies.values())

    def delete(self, company_id: str) -> None:
        self.get_by_id(company_id=company_id)
        self.companies.pop(company_id)
