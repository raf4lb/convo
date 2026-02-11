from src.application.interfaces import IChatUseCase
from src.domain.entities.chat import Chat
from src.helpers.helpers import get_now


class GetChatUseCase(IChatUseCase):
    def execute(self, chat_id: str) -> Chat:
        return self._chat_repository.get_by_id(chat_id=chat_id)


class ListChatsByCompanyUseCase(IChatUseCase):
    def execute(self, company_id: str) -> list[Chat]:
        return self._chat_repository.get_by_company_id(company_id=company_id)


class GetUnassignedChatsUseCase(IChatUseCase):
    def execute(self, company_id: str) -> list[Chat]:
        return self._chat_repository.get_unassigned_by_company_id(company_id=company_id)


class GetPendingChatsUseCase(IChatUseCase):
    def execute(self, company_id: str) -> list[Chat]:
        return self._chat_repository.get_pending_by_company_id(company_id=company_id)


class GetResolvedChatsUseCase(IChatUseCase):
    def execute(self, company_id: str) -> list[Chat]:
        return self._chat_repository.get_resolved_by_company_id(company_id=company_id)


class GetChatsByAttendantUseCase(IChatUseCase):
    def execute(self, company_id: str, attendant_id: str) -> list[Chat]:
        return self._chat_repository.get_by_attendant_id(
            company_id=company_id, attendant_id=attendant_id
        )


class SearchChatsUseCase(IChatUseCase):
    def execute(
        self, company_id: str, query: str, user_id: str | None = None
    ) -> list[Chat]:
        return self._chat_repository.search_chats(
            company_id=company_id, query=query, user_id=user_id
        )


class AssignAttendantToChatUseCase(IChatUseCase):
    def execute(self, chat_id: str, attendant_id: str | None) -> Chat:
        chat = self._chat_repository.get_by_id(chat_id=chat_id)
        chat.attached_user_id = attendant_id
        chat.updated_at = get_now()
        return self._chat_repository.save(chat)
