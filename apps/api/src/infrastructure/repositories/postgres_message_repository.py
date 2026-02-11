from src.domain.entities.message import Message
from src.domain.errors import MessageNotFoundError
from src.domain.repositories.message_repository import IMessageRepository
from src.infrastructure.daos.postgres_message_dao import PostgresMessageDAO


class PostgresMessageRepository(IMessageRepository):
    def __init__(self, message_dao: PostgresMessageDAO):
        self.message_dao = message_dao

    @staticmethod
    def _parse_row(row: tuple) -> Message:
        return Message(
            id=row[0],
            external_id=row[1],
            external_timestamp=row[2],
            chat_id=row[3],
            text=row[4],
            sent_by_user_id=row[5],
            read=row[6],
            created_at=row[7],
            updated_at=row[8],
        )

    def save(self, message: Message) -> Message:
        existing = self.message_dao.get_by_id(message_id=message.id)
        message_data = {
            "id": message.id,
            "external_id": message.external_id,
            "external_timestamp": message.external_timestamp,
            "chat_id": message.chat_id,
            "text": message.text,
            "sent_by_user_id": message.sent_by_user_id,
            "read": message.read,
            "created_at": message.created_at,
            "updated_at": message.updated_at,
        }

        if existing:
            row = self.message_dao.update(message_data)
        else:
            row = self.message_dao.insert(message_data)

        return self._parse_row(row=row)

    def get_by_id(self, message_id: str) -> Message:
        row = self.message_dao.get_by_id(message_id=message_id)
        if not row:
            raise MessageNotFoundError

        return self._parse_row(row=row)

    def get_by_external_id(self, external_id: str) -> Message | None:
        row = self.message_dao.get_by_external_id(external_id=external_id)
        if not row:
            return None

        return self._parse_row(row=row)

    def get_all(self) -> list[Message]:
        rows = self.message_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, message_id: str) -> None:
        self.get_by_id(message_id=message_id)
        self.message_dao.delete(message_id=message_id)

    def mark_chat_messages_as_read(self, chat_id: str) -> int:
        updated_count = self.message_dao.mark_chat_messages_as_read(chat_id=chat_id)
        return updated_count
