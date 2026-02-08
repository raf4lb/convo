from src.application.interfaces import IChatUseCase
from src.domain.entities.chat import Chat


class ListChatsByCompanyUseCase(IChatUseCase):
    def execute(self, company_id: str) -> list[Chat]:
        return self._chat_repository.get_by_company_id(company_id=company_id)
