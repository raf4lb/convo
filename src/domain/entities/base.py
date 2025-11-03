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
