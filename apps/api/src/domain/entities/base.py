from datetime import datetime

from src.helpers.helpers import get_now


class BaseEntity:
    def __init__(
        self,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.created_at = created_at or get_now()
        self.updated_at = updated_at


class UnsetType:
    """Sentinel type to represent a value not provided."""

    def __bool__(self):
        return False

    def __repr__(self):
        return "UNSET"


UNSET = UnsetType()
