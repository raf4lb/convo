import uuid
from datetime import UTC, datetime


def get_now() -> datetime:
    return datetime.now(UTC)


def generate_uuid4() -> str:
    return str(uuid.uuid4())
