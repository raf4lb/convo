from fastapi import FastAPI

from src.web.framework.app import create_app


def test_flask_app():
    assert isinstance(create_app(), FastAPI)
