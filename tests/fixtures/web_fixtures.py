import pytest
from fastapi.testclient import TestClient

from src.infrastructure.settings import AppSettings
from src.web.framework.app import create_app


@pytest.fixture
def app_settings():
    return AppSettings(
        DATABASE_NAME="DATABASE_NAME",
        DATABASE_USER="DATABASE_USER",
        DATABASE_PASSWORD="DATABASE_PASSWORD",
        DATABASE_URL="DATABASE_URL",
        WEBHOOK_VERIFY_TOKEN="WEBHOOK_VERIFY_TOKEN",
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
