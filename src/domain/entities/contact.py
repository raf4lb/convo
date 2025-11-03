from datetime import datetime

from src.domain.entities.base import BaseEntity


class Contact(BaseEntity):
    def __init__(
        self,
        id: str,
        name: str,
        phone_number: str,
        company_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.company_id = company_id
