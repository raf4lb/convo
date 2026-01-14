import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_URL: str
    WEBHOOK_VERIFY_TOKEN: str
    CORS_ORIGINS: list[str]


def load_settings():
    return AppSettings(
        DATABASE_NAME=os.getenv("DATABASE_NAME"),
        DATABASE_USER=os.getenv("DATABASE_USER"),
        DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD"),
        DATABASE_URL=os.getenv("DATABASE_URL"),
        WEBHOOK_VERIFY_TOKEN=os.getenv("WEBHOOK_VERIFY_TOKEN"),
        CORS_ORIGINS=os.getenv("CORS_ORIGINS").split(","),
    )
