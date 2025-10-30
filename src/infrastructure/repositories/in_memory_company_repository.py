from src.domain.entities.company import Company
from src.domain.errors import CompanyNotFoundError
from src.domain.repositories.company_repository import (
    ICompanyRepository,
)


class InMemoryCompanyRepository(ICompanyRepository):
    def __init__(self):
        self.companies = {}

    def save(self, company: Company) -> None:
        self.companies[company.id] = company

    def get_by_id(self, company_id: str) -> Company | None:
        company = self.companies.get(company_id)
        if company is None:
            raise CompanyNotFoundError
        return company

    def get_companies(self) -> list[Company]:
        return list(self.companies.values())

    def delete(self, company_id: str) -> None:
        try:
            self.companies.pop(company_id)
        except KeyError:
            raise CompanyNotFoundError
