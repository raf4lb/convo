from datetime import datetime

from src.domain.entities.base import BaseEntity


class Message(BaseEntity):
    def __init__(
        self,
        id: str,
        external_id: str,
        external_timestamp: datetime,
        chat_id: str,
        is_received: bool,
        text: str,
        received_by: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.external_id = external_id
        self.external_timestamp = external_timestamp
        self.chat_id = chat_id
        self.is_received = is_received
        self.text = text
        self.received_by = received_by
