from datetime import datetime

from src.domain.entities.company import Company
from src.domain.errors import CompanyNotFoundError
from src.domain.repositories.company_repository import (
    ICompanyRepository,
)


class InMemoryCompanyRepository(ICompanyRepository):
    def __init__(self):
        self.companies = {
            "474d2fd7-2e99-452b-a4db-fe93ecf8729c": Company(
                id="474d2fd7-2e99-452b-a4db-fe93ecf8729c",
                name="Tech Solutions Ltda",
                email="contato@techsolutions.com",
                phone="5511987654321",
                whatsapp_api_key="mock-api-key-123",
                created_at=datetime(2024, 1, 15),
                updated_at=datetime(2024, 1, 15),
                is_active=True,
                attendant_sees_all_conversations=True,
            ),
            "6dfaada5-37b1-442d-a21b-b63edf12bbd0": Company(
                id="6dfaada5-37b1-442d-a21b-b63edf12bbd0",
                name="Comércio Digital SA",
                email="contato@comerciodigital.com",
                phone="5521998765432",
                whatsapp_api_key="mock-api-key-456",
                created_at=datetime(2024, 2, 20),
                updated_at=datetime(2024, 2, 20),
                is_active=True,
                attendant_sees_all_conversations=False,
            ),
        }

    def save(self, company: Company) -> Company:
        self.companies[company.id] = company
        return company

    def get_by_id(self, company_id: str) -> Company:
        company = self.companies.get(company_id)
        if company is None:
            raise CompanyNotFoundError
        return company

    def get_all(self) -> list[Company]:
        return list(self.companies.values())

    def delete(self, company_id: str) -> None:
        self.get_by_id(company_id=company_id)
        self.companies.pop(company_id)
