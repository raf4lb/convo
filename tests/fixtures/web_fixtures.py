import pytest
from fastapi.testclient import TestClient

from src.web.framework.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
