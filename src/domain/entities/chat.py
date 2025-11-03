from datetime import datetime

from src.domain.entities.base import BaseEntity
from src.domain.enums import ChatStatuses


class Chat(BaseEntity):
    def __init__(
        self,
        id: str,
        company_id: str,
        contact_id: str,
        status: ChatStatuses = ChatStatuses.OPEN,
        attached_user_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.company_id = company_id
        self.contact_id = contact_id
        self.status = status
        self.attached_user_id = attached_user_id
