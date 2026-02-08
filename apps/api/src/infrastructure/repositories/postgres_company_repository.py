from src.domain.entities.company import Company
from src.domain.errors import CompanyNotFoundError
from src.domain.repositories.company_repository import ICompanyRepository
from src.infrastructure.daos.postgres_company_dao import PostgresCompanyDAO


class PostgresCompanyRepository(ICompanyRepository):
    def __init__(self, company_dao: PostgresCompanyDAO):
        self._company_dao = company_dao

    @staticmethod
    def _parse_row(row: tuple) -> Company:
        return Company(
            id=row[0],
            name=row[1],
            created_at=row[2],
            updated_at=row[3],
            email=row[4],
            phone=row[5],
            is_active=row[6],
            attendant_sees_all_conversations=row[7],
            whatsapp_api_key=row[8],
        )

    def save(self, company: Company) -> None:
        existing = self._company_dao.get_by_id(company_id=company.id)
        company_data = {
            "id": company.id,
            "name": company.name,
            "email": company.email,
            "phone": company.phone,
            "is_active": company.is_active,
            "attendant_sees_all_conversations": company.attendant_sees_all_conversations,
            "whatsapp_api_key": company.whatsapp_api_key,
            "created_at": company.created_at,
            "updated_at": company.updated_at,
        }

        if existing:
            self._company_dao.update(company_data)
        else:
            self._company_dao.insert(company_data)

    def get_by_id(self, company_id: str) -> Company:
        row = self._company_dao.get_by_id(company_id=company_id)
        if not row:
            raise CompanyNotFoundError

        return self._parse_row(row=row)

    def get_all(self) -> list[Company]:
        rows = self._company_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, company_id: str) -> None:
        self.get_by_id(company_id=company_id)
        self._company_dao.delete(company_id=company_id)
