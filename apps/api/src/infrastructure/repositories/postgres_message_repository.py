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
            created_at=row[6],
            updated_at=row[7],
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
            "created_at": message.created_at,
            "updated_at": message.updated_at,
        }

        if existing:
            self.message_dao.update(message_data)
        else:
            self.message_dao.insert(message_data)

        return message

    def get_by_id(self, message_id: str) -> Message:
        row = self.message_dao.get_by_id(message_id=message_id)
        if not row:
            raise MessageNotFoundError

        return self._parse_row(row=row)

    def get_all(self) -> list[Message]:
        rows = self.message_dao.get_all()
        return [self._parse_row(row=row) for row in rows]

    def delete(self, message_id: str) -> None:
        self.get_by_id(message_id=message_id)
        self.message_dao.delete(message_id=message_id)
