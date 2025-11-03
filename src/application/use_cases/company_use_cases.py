from src.application.interfaces import ICompanyUseCase
from src.domain.entities.company import Company
from src.helpers.helpers import generate_uuid4, get_now


class CreateCompanyUseCase(ICompanyUseCase):
    def execute(
        self,
        name: str,
    ) -> Company:
        company = Company(
            id=generate_uuid4(),
            name=name,
        )
        self._company_repository.save(company)
        return company


class UpdateCompanyUseCase(ICompanyUseCase):
    def execute(self, company_id: str, name: str) -> Company:
        company = self._company_repository.get_by_id(company_id)
        company.name = name
        company.updated_at = get_now()
        self._company_repository.save(company)
        return company


class GetCompanyUseCase(ICompanyUseCase):
    def execute(self, company_id) -> Company:
        return self._company_repository.get_by_id(company_id=company_id)


class DeleteCompanyUseCase(ICompanyUseCase):
    def execute(self, company_id: str) -> None:
        self._company_repository.delete(company_id)


class ListCompanyUseCase(ICompanyUseCase):
    def execute(self) -> list[Company]:
        return self._company_repository.get_all()
