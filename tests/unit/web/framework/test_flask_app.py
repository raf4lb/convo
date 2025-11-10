from flask import Flask

from src.web.framework.flask_app import create_app


def test_flask_app():
    assert isinstance(create_app(), Flask)
