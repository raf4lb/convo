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
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECURE_COOKIES: bool


def load_settings() -> AppSettings:
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
        JWT_SECRET=os.getenv("JWT_SECRET", "dev-secret-change-in-production"),
        JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
        ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")),
        REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
        SECURE_COOKIES=os.getenv("SECURE_COOKIES", "false").lower() == "true",
    )
