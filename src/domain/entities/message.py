from datetime import datetime

from src.domain.entities.base import BaseEntity


class Message(BaseEntity):
    def __init__(
        self,
        id: str,
        external_id: str,
        external_timestamp: datetime,
        chat_id: str,
        text: str,
        sent_by_user_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.external_id = external_id
        self.external_timestamp = external_timestamp
        self.chat_id = chat_id
        self.text = text
        self.sent_by_user_id = sent_by_user_id

    def is_from_contact(self) -> bool:
        """Returns True if message was sent by the contact (customer)."""
        return self.sent_by_user_id is None

    def is_from_user(self) -> bool:
        """Returns True if message was sent by a user (company attendant)."""
        return self.sent_by_user_id is not None
