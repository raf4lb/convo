import pytest
from fastapi.testclient import TestClient

from src.infrastructure.enums import DatabaseType
from src.infrastructure.settings import AppSettings
from src.web.framework.app import create_app


@pytest.fixture
def app_settings():
    return AppSettings(
        DATABASE_TYPE=DatabaseType.INMEMORY,
        DATABASE_NAME="DATABASE_NAME",
        DATABASE_USER="DATABASE_USER",
        DATABASE_PASSWORD="DATABASE_PASSWORD",
        DATABASE_URL="DATABASE_URL",
        WEBHOOK_VERIFY_TOKEN="WEBHOOK_VERIFY_TOKEN",
        CORS_ORIGINS=[],
        JWT_SECRET="test-secret-key",
        JWT_ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=15,
        REFRESH_TOKEN_EXPIRE_DAYS=7,
        SECURE_COOKIES=False,
    )


@pytest.fixture
def app(app_settings):
    app = create_app()
    app.state.settings = app_settings
    return app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
