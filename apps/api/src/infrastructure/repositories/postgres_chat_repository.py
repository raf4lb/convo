from src.domain.entities.chat import Chat
from src.domain.enums import ChatStatuses
from src.domain.errors import ChatNotFoundError
from src.domain.repositories.chat_repository import IChatRepository
from src.infrastructure.daos.postgres_chat_dao import PostgresChatDAO


class PostgresChatRepository(IChatRepository):
    def __init__(self, chat_dao: PostgresChatDAO):
        self._chat_dao = chat_dao

    @staticmethod
    def _parse_row(row: tuple) -> Chat:
        return Chat(
            id=row[0],
            company_id=row[1],
            contact_id=row[2],
            status=ChatStatuses(row[3]),
            attached_user_id=row[4],
            created_at=row[5],
            updated_at=row[6],
        )

    def save(self, chat: Chat) -> Chat:
        existing = self._chat_dao.get_by_id(chat_id=chat.id)
        chat_data = {
            "id": chat.id,
            "contact_id": chat.contact_id,
            "status": chat.status.value,
            "company_id": chat.company_id,
            "attached_user_id": chat.attached_user_id,
            "created_at": chat.created_at,
            "updated_at": chat.updated_at,
        }

        if existing:
            row = self._chat_dao.update(chat_data)
        else:
            row = self._chat_dao.insert(chat_data)

        return self._parse_row(row=row)

    def get_by_id(self, chat_id: str) -> Chat:
        row = self._chat_dao.get_by_id(chat_id)
        if not row:
            raise ChatNotFoundError

        return self._parse_row(row=row)

    def get_all(self) -> list[Chat]:
        rows = self._chat_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def get_by_company_id(self, company_id: str) -> list[Chat]:
        rows = self._chat_dao.get_by_company_id(company_id=company_id)
        return [self._parse_row(row=row) for row in rows]

    def get_company_chat_by_contact_id(
        self,
        company_id: str,
        contact_id: str,
    ) -> Chat:
        row = self._chat_dao.get_company_chat_by_contact_id(
            company_id=company_id,
            contact_id=contact_id,
        )
        if not row:
            raise ChatNotFoundError

        return self._parse_row(row=row)

    def delete(self, chat_id: str) -> None:
        self.get_by_id(chat_id=chat_id)
        self._chat_dao.delete(chat_id)

    def get_unassigned_by_company_id(self, company_id: str) -> list[Chat]:
        rows = self._chat_dao.get_unassigned_by_company_id(company_id=company_id)
        return [self._parse_row(row=row) for row in rows]

    def get_by_attendant_id(self, company_id: str, attendant_id: str) -> list[Chat]:
        rows = self._chat_dao.get_by_attendant_id(
            company_id=company_id, attendant_id=attendant_id
        )
        return [self._parse_row(row=row) for row in rows]

    def search_chats(
        self, company_id: str, query: str, user_id: str | None = None
    ) -> list[Chat]:
        rows = self._chat_dao.search_chats(
            company_id=company_id, query=query, user_id=user_id
        )
        return [self._parse_row(row=row) for row in rows]
