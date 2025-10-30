from flask import Flask

from src.infrastructure.repositories.in_memory_company_repository import (
    InMemoryCompanyRepository,
)
from src.infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from src.web.framework.routes.user_routes import user_route_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_route_blueprint, url_prefix="/users")

    app.config["user_repository"] = InMemoryUserRepository()
    app.config["company_repository"] = InMemoryCompanyRepository()

    return app
