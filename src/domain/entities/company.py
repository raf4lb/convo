from datetime import datetime

from src.domain.entities.base import BaseEntity


class Company(BaseEntity):
    def __init__(
        self,
        id: str,
        name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.name = name
