from datetime import datetime
from uuid import UUID

from src.domain.entities.base import BaseEntity
from src.domain.enums import UserTypes


class User(BaseEntity):
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        type: UserTypes,
        company_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(created_at=created_at, updated_at=updated_at)
        self.id = id
        self.name = name
        self.email = email
        self.type = type
        self.company_id = company_id

    def validate(self) -> list[str]:
        errors = []
        try:
            UUID(self.id)
        except (ValueError, TypeError):
            errors.append("invalid id")

        if self.company_id is not None:
            try:
                UUID(self.company_id)
            except (ValueError, TypeError):
                errors.append("invalid company id")

        try:
            UserTypes(self.type)
        except ValueError:
            errors.append("invalid user type")

        if not isinstance(self.name, str):
            errors.append("invalid name")

        if not isinstance(self.email, str):
            errors.append("invalid email")

        if not isinstance(self.created_at, datetime):
            errors.append("invalid created at")

        if self.updated_at and not isinstance(self.updated_at, datetime):
            errors.append("invalid updated at")

        return errors
