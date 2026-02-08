import os
from dataclasses import dataclass

from src.infrastructure.enums import DatabaseType


@dataclass(frozen=True)
class AppSettings:
    DATABASE_TYPE: DatabaseType
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_URL: str
    WEBHOOK_VERIFY_TOKEN: str
    CORS_ORIGINS: list[str]


def load_settings():
    db_type_str = os.getenv("DATABASE_TYPE", "inmemory")
    try:
        database_type = DatabaseType(db_type_str)
    except ValueError:
        raise ValueError(
            f"Invalid DATABASE_TYPE: {db_type_str}. "
            f"Valid options: {', '.join([t.value for t in DatabaseType])}"
        )

    return AppSettings(
        DATABASE_TYPE=database_type,
        DATABASE_NAME=os.getenv("DATABASE_NAME"),
        DATABASE_USER=os.getenv("DATABASE_USER"),
        DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD"),
        DATABASE_URL=os.getenv("DATABASE_URL"),
        WEBHOOK_VERIFY_TOKEN=os.getenv("WEBHOOK_VERIFY_TOKEN"),
        CORS_ORIGINS=os.getenv("CORS_ORIGINS").split(","),
    )
