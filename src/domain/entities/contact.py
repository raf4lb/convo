from datetime import datetime

from src.domain.entities.base import BaseEntity


class Contact(BaseEntity):
    def __init__(
        self,
        id: str,
        name: str,
        phone_number: str,
        email: str | None = None,
        company_id: str | None = None,
        last_contact_at: datetime | None = None,
        is_blocked: bool = False,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.company_id = company_id
        self.last_contact_at = last_contact_at
        self.is_blocked = is_blocked
