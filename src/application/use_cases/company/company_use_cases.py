import uuid

from src.application.interfaces.use_case_interface import IUseCase
from src.domain.entities.company import Company
from src.domain.repositories.company_repository import (
    ICompanyRepository,
)
from src.helpers.helpes import get_now_iso_format


class CreateCompanyUseCase(IUseCase):
    def __init__(self, repository: ICompanyRepository):
        self._repository = repository

    def execute(
        self,
        name: str,
    ) -> Company:
        created_at = get_now_iso_format()
        company = Company(
            id=str(uuid.uuid4()),
            name=name,
            created_at=created_at,
            updated_at=created_at,
        )
        self._repository.save(company)
        return company


class UpdateCompanyUseCase(IUseCase):
    def __init__(self, repository: ICompanyRepository):
        self._repository = repository

    def execute(self, company_id: str, name: str) -> Company:
        company = self._repository.get_company_by_id(company_id)
        company.name = name
        company.updated_at = get_now_iso_format()
        self._repository.save(company)
        return company
