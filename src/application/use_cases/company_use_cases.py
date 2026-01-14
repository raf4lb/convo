from src.application.interfaces import ICompanyUseCase
from src.domain.entities.company import Company
from src.helpers.helpers import generate_uuid4, get_now


class CreateCompanyUseCase(ICompanyUseCase):
    def execute(
        self,
        name: str,
        email: str,
        phone: str,
        is_active: bool = True,
        attendant_sees_all_conversations: bool = True,
        whatsapp_api_key: str | None = None,
    ) -> Company:
        company = Company(
            id=generate_uuid4(),
            name=name,
            email=email,
            phone=phone,
            whatsapp_api_key=whatsapp_api_key,
            is_active=is_active,
            attendant_sees_all_conversations=attendant_sees_all_conversations,
        )
        self._company_repository.save(company)
        return company


class UpdateCompanyUseCase(ICompanyUseCase):
    def execute(
        self,
        company_id: str,
        name: str,
        email: str,
        phone: str,
        is_active: bool = True,
        attendant_sees_all_conversations: bool = True,
        whatsapp_api_key: str | None = None,
    ) -> Company:
        company = self._company_repository.get_by_id(company_id)
        if name is not None:
            company.name = name
        if email is not None:
            company.email = email
        if phone is not None:
            company.phone = phone
        if is_active is not None:
            company.is_active = is_active
        if attendant_sees_all_conversations is not None:
            company.attendant_sees_all_conversations = attendant_sees_all_conversations
        if whatsapp_api_key is not None:
            company.whatsapp_api_key = whatsapp_api_key
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
